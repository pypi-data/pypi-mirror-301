import json
import threading
from datetime import datetime, timezone
from loguru import logger
from celery.events.state import Task, states, Worker
from celery.events import EventReceiver
from .nocodb import NocodbClient


class Monitor(threading.Thread):

    def __init__(self, app, nocodb: NocodbClient):
        threading.Thread.__init__(self)
        self.app = app
        self.state = app.events.State()
        self.nocodb = nocodb
        self.tables = self.nocodb.get_tables()
        self.worker_table_id = self.tables["Worker"]
        self.task_table_id = self.tables["Task"]
        self.should_stop = False
        self.daemon = True
        self._uuid_cache = {}        # 缓存uuid和nocodb中的Id
        self._update_task_lock = threading.Lock()
        logger.info("Celery event monitor thread started")

    def add_new_task_to_nocodb(self, record: dict):
        """新增任务到 nocodb, 并将 uuid 缓存到本地
    
        主要为了处理PENDING状态task信息不入库的问题
        record: dict
            {
                "task_id": "task_id",
                "name": "task_name",
                "args": [],
                "kwargs": {},
                "state": "PENDING",
                "queue": ""
            }
        """
        if "timestamp" in record:
            record["timestamp"] = datetime.fromtimestamp(record["timestamp"], tz=timezone.utc).isoformat()
        
        return self._add_or_update_task_to_nocodb(record)

    def _add_worker_to_nocodb(self, worker):
        """worker schema in nocodb
        {
            'hostname': 'worker@notmmao', 'utcoffset': -8, 
            'pid': 24076, 'clock': 9, 'freq': 2.0, 'active': 0, 
            'processed': 0, 'loadavg': [0.0, 0.0, 0.0], 
            'sw_ident': 'py-celery', 'sw_ver': '5.2.7', 'sw_sys': 'Windows', 
            'timestamp': 1728550831.797462, 'local_received': 1728550831.8085027,
            'type': 'worker-offline', 
        }
        """
        # worker.pop("local_received")
        if "timestamp" in worker:
            worker["timestamp"] = datetime.fromtimestamp(worker["timestamp"], tz=timezone.utc).isoformat()
        if "local_received" in worker:
            worker["local_received"] = datetime.fromtimestamp(worker["local_received"], tz=timezone.utc).isoformat()
        self.nocodb.add_one(self.worker_table_id, worker, key="hostname", update_if_exists=True)

    def _add_task_to_nocodb(self, task: Task):
        """
        将任务添加到 NocoDB 中。

        此方法将任务记录添加到 NocoDB 数据库中。如果任务已经存在，则更新现有记录。

        参数:
            task (Task): 要添加或更新的任务对象。

        返回:
            dict: 包含 NocoDB 响应的字典。

        记录结构:
            - task_id: 任务的唯一标识符
            - name: 任务名称
            - state: 任务状态
            - result: 任务结果
            - args: 任务参数
            - kwargs: 任务关键字参数
            - exception: 任务异常信息
            - traceback: 任务异常追踪
            - timestamp: 任务时间戳
            - eta: 任务预计执行时间
            - retries: 任务重试次数
            - worker: 执行任务的工作节点

        如果任务记录已经存在，使用任务 ID 从缓存中获取记录 ID 并更新记录。
        否则，添加新记录并将记录 ID 缓存起来。
        """
        record = {
            "task_id": task.id,
            "name": task.name,
            "state": task.state,
            "result": task.result,
            "args": task.args,
            "kwargs": task.kwargs,
            "exception": task.exception,
            "traceback": task.traceback,
            # "timestamp": task.timestamp,
            # "worker": repr(task.worker),
            "eta": task.eta,
            "retries": task.retries,
        }
        if task.timestamp:
            record["timestamp"] = datetime.fromtimestamp(task.timestamp, tz=timezone.utc).isoformat()
        if task.worker:
            # celery.events.state.Worker
            record["worker"] = repr(task.worker)
        return self._add_or_update_task_to_nocodb(record)
        
    def _add_or_update_task_to_nocodb(self, record:dict):
        """
        将任务记录添加到 NocoDB 数据库中。
        如果任务记录已经存在，使用任务 ID 从缓存中获取记录 ID 并更新记录。
        否则，添加新记录并将记录 ID 缓存起来。
        
        此函数加了锁, 所有更新task的操作都应该调用次函数, 以避免多线程冲突.
        """
        with self._update_task_lock:
            task_id = record["task_id"]
            record_id = self._uuid_cache.get(task_id)
            if record_id:
                record["Id"] = record_id
                resp = self.nocodb.update(self.task_table_id, record)
                logger.debug("update task {} to nocodb", record)
            else:
                resp = self.nocodb.add_one(self.task_table_id, record, key="task_id", update_if_exists=True)
                logger.debug("add task {} to nocodb", record)
                self._uuid_cache[task_id] = resp["Id"]
            return resp

    def run(self):
        while not self.should_stop:
            try:
                self._run()
            except Exception as e:
                logger.error(f"Error in monitor thread: {e}, retrying...")
                continue

    def _run(self):
        with self.app.connection() as connection:
            recv : EventReceiver = self.app.events.Receiver(connection, handlers={
                'task-send': self.on_task_event,
                'task-received': self.on_task_event,
                'task-started': self.on_task_event,
                'task-progress': self.on_task_event_custom,    # 自定义处理进度
                'task-succeeded': self.on_task_event,
                'task-failed': self.on_task_event,
                'task-rejected': self.on_task_event,
                'task-revoked': self.on_task_event,
                'task-retried': self.on_task_event,
                'worker-online': self.on_worker_event,
                'worker-offline': self.on_worker_event,
                'worker-heartbeat': self.on_worker_event,
                # 'worker-heartbeat': self.state.event,   # 默认处理程序
                '*': self.state.event,   # 默认处理程序
            })
            logger.info("Celery event Monitor thread connected to broker")
            recv.capture(limit=None, timeout=None, wakeup=True)

    def on_worker_event(self, event):
        self.state.event(event)
        logger.debug(f"Worker: event {event}")
        self._add_worker_to_nocodb(event)

    def on_task_event_custom(self, event):
        self.state.event(event)
        logger.info("Task: event {}", event)
        if 'uuid' not in event:
            logger.warning("Task event without uuid {}", event)
            return
        if event['type'] == 'task-progress':
            # 自定义处理进度
            record = {
                "task_id": event["uuid"],
                "meta": json.dumps(event.get("meta", {})),
                "state": event["state"]
            }
            return self._add_or_update_task_to_nocodb(record)

    def on_task_event(self, event):
        self.state.event(event)
        task: Task = self.state.tasks.get(event['uuid'])
        self._add_task_to_nocodb(task)
        if task.state in states.EXCEPTION_STATES:
            logger.warning(f"Task: {task.state} {task.info()}")
        else:
            logger.debug(f"Task: {task.state} {task.info()}")
            
