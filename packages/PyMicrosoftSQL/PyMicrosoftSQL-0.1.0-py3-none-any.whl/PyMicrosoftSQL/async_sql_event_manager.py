import threading
import queue
import time
import ctypes
from PyMicrosoftSQL.constants import ConstantsODBC as const

class Event:
    def __init__(self, handle=None, event_type=None):
        self.listening = False
        self.signaled = False
        self.last_checked_at = time.time()
        self.cond = threading.Condition()
        self.handle = handle
        self.event_type = event_type

    def signal(self):
        with self.cond:
            self.signaled = True
            self.listening = False
            self.cond.notify_all()
            
    def wait(self):
        with self.cond:
            while self.listening and not self.signaled:
                self.cond.wait()
            self.signaled = False
            
class AsyncSQLEventManager:
    def __init__(self, sql_driver_connect, sql_exec_direct):
        self.conn_queue = queue.PriorityQueue()
        self.stmt_queue = queue.PriorityQueue()
        self.conn_events_running = False
        self.stmt_events_running = False
        self.heartbeat = Heartbeat()
        self.lock = threading.Lock() # mutex lock
        self.sql_driver_connect = sql_driver_connect
        self.sql_exec_direct = sql_exec_direct
        self.check_and_run_monitor()

    def add_conn_handle(self, event):
        with self.lock:
            self.conn_queue.put(event)
            event.listening = True
            if not self.conn_events_running:
                self.conn_events_running = True
                threading.Thread(target=self.conn_events_check, daemon=True).start()

    def add_stmt_handle(self, event):
        with self.lock:
            self.stmt_queue.put(event)
            event.listening = True
            if not self.stmt_events_running:
                self.stmt_events_running = True
                threading.Thread(target=self.stmt_events_check, daemon=True).start()

    def conn_events_check(self):
        while True:
            with self.lock:
                if self.conn_queue.empty():
                    self.conn_events_running = False
                    break
                event = self.conn_queue.get()
            self.check_and_run_monitor()
            time.sleep(0.2)
            try:
                retcode = self.sql_driver_connect(event.handle, None, None, 0, None, 0, None, 0)
                with self.lock:
                    self.conn_queue.task_done()
                    if retcode == const.SQL_STILL_EXECUTING:
                        event.last_checked_at = time.time()
                        self.conn_queue.put(event)
                    else:
                        event.signal()
            except Exception as ex:
                event.signal()
                self.conn_events_running = False

    def stmt_events_check(self):
        while True:
            with self.lock:
                if self.stmt_queue.empty():
                    self.stmt_events_running = False
                    break
                event = self.stmt_queue.get()
            self.check_and_run_monitor()
            time.sleep(0.2)
            try:
                retcode = self.sql_exec_direct(event.handle, ctypes.c_wchar_p(""), const.SQL_NTS)
                with self.lock:
                    self.stmt_queue.task_done()
                    if retcode == const.SQL_STILL_EXECUTING:
                        event.last_checked_at = time.time()
                        self.stmt_queue.put(event)
                    else:
                        event.signal()
            except Exception as ex:
                event.signal()
                self.stmt_events_running = False

    def monitor_task(self):
        while True:
            with self.lock:
                if not self.conn_events_running and not self.conn_queue.empty():
                    self.conn_events_running = True
                    threading.Thread(target=self.conn_events_check, daemon=True).start()
                if not self.stmt_events_running and not self.stmt_queue.empty():
                    self.stmt_events_running = True
                    threading.Thread(target=self.stmt_events_check, daemon=True).start()
            time.sleep(2)

    def check_and_run_monitor(self):
        if not hasattr(self, 'monitor_thread') or not self.monitor_thread.is_alive():
            self.monitor_thread = threading.Thread(target=self.monitor_task, daemon=True)
            self.monitor_thread.start()

class Heartbeat:
    def __init__(self):
        self.monitor_heartbeat = time.time()
        self.conn_heartbeat = time.time()
        self.stmt_heartbeat = time.time()