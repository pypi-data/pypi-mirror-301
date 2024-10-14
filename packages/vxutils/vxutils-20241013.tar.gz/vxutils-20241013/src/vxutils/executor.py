"""Implements a thread pool executor."""

__author__ = "vex1023 (libao@vxquant.com)"
from contextlib import suppress
import os
import time
import uuid
import logging
import itertools
from datetime import datetime, timedelta
import queue
import threading

from functools import wraps
from enum import Enum
from heapq import heappop, heappush
from concurrent.futures import Future, BrokenExecutor, Executor
from typing import (
    Any,
    Callable,
    List,
    Optional,
    Type,
    Set,
    Sequence,
    Iterable,
    Literal,
    Tuple,
    Generator,
)
from typing_extensions import Annotated, no_type_check
from pydantic import Field, PlainValidator
from vxutils.convertors import to_datetime, to_enum
from vxutils.context import VXContext
from vxutils.datamodel.core import VXDataModel


_delta = 0.1


class BrokenThreadPool(BrokenExecutor):
    pass


class VXTaskItem:
    def __init__(
        self,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.future: Future[Any] = Future()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, context: VXContext) -> None:
        if not self.future.set_running_or_notify_cancel():
            return

        try:
            result = self.func(*self.args, **self.kwargs)
            self.future.set_result(result)
        except Exception as exc:
            self.future.set_exception(exc)
            logging.error("task error: %s", exc, exc_info=True)


class TriggerStatus(Enum):
    """事件状态"""

    PENDING = "Pending"
    RUNNING = "Running"
    COMPLETE = "COMPLETE"
    UNKNOWN = "UNKNOWN"


class VXTrigger(VXDataModel):
    trigger_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    trigger_dt: Annotated[datetime, PlainValidator(lambda x: to_datetime(x))] = Field(
        default_factory=datetime.now
    )
    interval: float = 0

    start_dt: Annotated[datetime, PlainValidator(lambda x: to_datetime(x))] = Field(
        default_factory=datetime.now
    )
    end_dt: Annotated[datetime, PlainValidator(lambda x: to_datetime(x))] = Field(
        default=datetime.max
    )
    status: Annotated[
        TriggerStatus, PlainValidator(lambda v: to_enum(v, TriggerStatus.PENDING))
    ] = TriggerStatus.PENDING

    @no_type_check
    def model_post_init(self, __context: Any) -> None:
        if self.start_dt > self.end_dt:
            raise ValueError("开始时间不能大于结束时间")

        if self.status != TriggerStatus.PENDING:
            return
        return super().model_post_init(__context)

    def __lt__(self, other: "VXTrigger") -> bool:
        return self.trigger_dt < other.trigger_dt

    def _get_first_trigger_dt(self) -> Tuple[datetime, TriggerStatus]:
        if self.interval == 0:
            return self.start_dt, TriggerStatus.RUNNING

        if self.end_dt < datetime.now() + timedelta(seconds=_delta):
            return datetime.max, TriggerStatus.COMPLETE

        if self.start_dt.timestamp() + _delta >= time.time():
            return self.start_dt, TriggerStatus.RUNNING

        trigger_dt = datetime.fromtimestamp(
            self.start_dt.timestamp()
            + self.interval
            * ((time.time() - self.start_dt.timestamp()) // self.interval + 1)
        )
        if trigger_dt > self.end_dt:
            return datetime.max, TriggerStatus.COMPLETE
        else:
            return trigger_dt, TriggerStatus.RUNNING

    def _get_next_trigger_dt(self) -> Tuple[datetime, TriggerStatus]:
        if self.interval == 0 or self.status == TriggerStatus.COMPLETE:
            return datetime.max, TriggerStatus.COMPLETE

        trigger_dt = self.trigger_dt + timedelta(seconds=self.interval)
        if self.trigger_dt + timedelta(seconds=self.interval) > (
            self.end_dt - timedelta(seconds=_delta)
        ):
            return datetime.max, TriggerStatus.COMPLETE
        else:
            return trigger_dt, TriggerStatus.RUNNING

    def __next__(self) -> "VXTrigger":
        if self.status == TriggerStatus.PENDING:
            self.trigger_dt, self.status = self._get_first_trigger_dt()
        elif self.status == TriggerStatus.RUNNING:
            self.trigger_dt, self.status = self._get_next_trigger_dt()
        if self.status == TriggerStatus.COMPLETE:
            raise StopIteration

        return self

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        return self

    @classmethod
    @no_type_check
    def once(cls, trigger_dt: Optional[datetime] = None) -> "VXTrigger":
        if trigger_dt is None:
            trigger_dt = datetime.now()
        data = {
            "status": "Pending",
            "trigger_dt": trigger_dt,
            "start_dt": trigger_dt,
            "end_dt": trigger_dt,
            "interval": 0,
            "skip_holiday": False,
        }
        return cls(**data)

    @classmethod
    @no_type_check
    def every(
        cls,
        interval: float,
        *,
        start_dt: Optional[datetime] = None,
        end_dt: Optional[datetime] = None,
        skip_holiday: bool = False,
    ) -> "VXTrigger":
        if not start_dt:
            start_dt = datetime.now()
        if not end_dt:
            end_dt = datetime.max
        data = {
            "status": "Pending",
            "trigger_dt": start_dt,
            "start_dt": start_dt,
            "end_dt": end_dt,
            "interval": interval,
            "skip_holiday": skip_holiday,
        }
        return cls(**data)

    @classmethod
    @no_type_check
    def daily(
        cls,
        timestr: str = "00:00:00",
        freq: int = 1,
        *,
        start_dt: Optional[datetime] = None,
        end_dt: Optional[datetime] = None,
        skip_holiday: bool = False,
    ) -> "VXTrigger":
        """创建每日执行的触发器

        Keyword Arguments:
            timestr {str} -- 时间点 (default: {"00:00:00"})
            freq {int} -- 日期间隔，单位：天 (default: {1})
            start_dt {Optional[VXDatetime]} -- 开始时间 (default: {None})
            end_dt {Optional[VXDatetime]} -- 结束事件 (default: {None})
            skip_holiday {bool} -- 是否跳过工作日 (default: {False})

        Returns:
            VXTrigger -- 触发器
        """
        if not start_dt:
            start_dt = datetime.now()
        if not end_dt:
            end_dt = datetime.max
        data = {
            "status": "Pending",
            "trigger_dt": start_dt,
            "start_dt": start_dt.combine(
                start_dt.date(), datetime.strptime(timestr, "%H:%M:%S").time()
            ),
            "end_dt": end_dt,
            "interval": 86400 * freq,
            "skip_holiday": skip_holiday,
        }

        return cls(**data)


ONCE = VXTrigger.once
EVERY = VXTrigger.every
DAILY = VXTrigger.daily


class VXSchedTaskQueue(queue.Queue[Tuple[VXTrigger, Any]]):
    """任务队列"""

    def _init(self, maxsize: int = 0) -> None:
        self.queue: List[Tuple[VXTrigger, Any]] = []

    def _qsize(self) -> int:
        now = datetime.now()
        return len([1 for t, e in self.queue if t.trigger_dt <= now])

    @no_type_check
    def put(
        self,
        item: Any,
        block: bool = True,
        timeout: Optional[float] = None,
        *,
        trigger: Optional[VXTrigger] = None,
    ) -> None:
        if not trigger:
            trigger = VXTrigger.once()
        return super().put((trigger, item), block, timeout)

    @no_type_check
    def _put(self, item: Tuple[VXTrigger, Any]) -> None:
        with suppress(StopIteration):
            next(item[0])
            heappush(self.queue, item)

    def _get(self) -> Any:
        trigger, task = heappop(self.queue)
        if trigger.status == TriggerStatus.RUNNING and task is not None:
            new_task = VXTaskItem(task.func, *task.args, **task.kwargs)
            self._put((trigger, new_task))
            self.unfinished_tasks += 1
            self.not_empty.notify()
        return task

    def get(self, block: bool = True, timeout: Optional[float] = None) -> Any:
        """Remove and return an item from the queue.

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until an item is available. If 'timeout' is
        a non-negative number, it blocks at most 'timeout' seconds and raises
        the Empty exception if no item was available within that time.
        Otherwise ('block' is false), return an item if one is immediately
        available, else raise the Empty exception ('timeout' is ignored
        in that case).
        """
        with self.not_empty:
            if not block and (not self._qsize()):
                raise queue.Empty

            if timeout is not None and timeout <= 0:
                raise ValueError("'timeout' must be a non-negative number")

            if timeout is not None:
                endtime = time.time() + timeout
            else:
                endtime = float("inf")

            while not self._qsize():
                now = time.time()
                if now >= endtime:
                    raise queue.Empty

                lastest_trigger_dt = (
                    endtime
                    if len(self.queue) == 0
                    else self.queue[0][0].trigger_dt.timestamp()
                )
                min_endtime = min(endtime, lastest_trigger_dt, now + 1)
                remaining = min_endtime - now
                self.not_empty.wait(remaining)
            item = self._get()
            self.not_full.notify()
            return item


class VXBasicWorkerFactory(threading.Thread):
    """工作线程基类

    Arguments:
        work_queue {queue.Queue[VXTaskItem]} -- 任务队列
        idle_semaphore {threading.Semaphore} -- 信号量
        context {Optional[VXContext]} -- 上下文
        name {str} -- 线程名称
        idle_timeout {int} -- 空闲超时时间
    """

    def __init__(
        self,
        work_queue: queue.Queue[Optional[VXTaskItem]],
        idle_semaphore: threading.Semaphore,
        context: Optional[VXContext] = None,
        name: str = "",
        idle_timeout: Optional[int] = None,
    ) -> None:
        self._idle_semaphore = idle_semaphore
        self._idle_timeout = idle_timeout
        self._work_queue = work_queue
        self._context = context if context is not None else VXContext()
        return super().__init__(name=name, daemon=True, target=self.__worker_run__)

    @property
    def context(self) -> VXContext:
        """上下文"""
        return self._context

    def pre_run(self) -> None:
        logging.debug("worker %s start...", self.name)

    def post_run(self) -> None:
        logging.debug("worker %s stop...", self.name)

    def __worker_run__(self) -> None:
        try:
            self.pre_run()
        except BaseException as err:
            logging.error("worker pre_run error: %s", err, exc_info=True)
            raise BrokenThreadPool(err)

        try:
            while True:
                is_idle = False

                if self._work_queue.empty():
                    self._idle_semaphore.release()
                    is_idle = True
                task = self._work_queue.get(timeout=self._idle_timeout)
                logging.debug("worker %s get task: %s", self.name, task)
                if task is None:
                    return
                with suppress(Exception):
                    task(self.context)

        except queue.Empty:
            pass
        except KeyboardInterrupt:
            logging.error("worker KeyboardInterrupt")
        finally:
            if is_idle:
                self._idle_semaphore.acquire(blocking=False)
            self.post_run()


def _result_or_cancel(fut: Future[Any], timeout: Optional[float] = None) -> Any:
    try:
        try:
            return fut.result(timeout)
        finally:
            fut.cancel()
    finally:
        # Break a reference cycle with the exception in self._exception
        del fut


class VXSchedExecutor(Executor):
    _counter = itertools.count().__next__

    def __init__(
        self,
        max_workers: Optional[int] = None,
        thread_name_prefix: str = "",
        *,
        context: Optional[VXContext] = None,
        idle_timeout: int = 600,
        worker_factory: Type[VXBasicWorkerFactory] = VXBasicWorkerFactory,
    ) -> None:
        """Initializes a new VXExecutor instance.

        Args:
            max_workers: The maximum number of threads that can be used to
                execute the given calls.
            thread_name_prefix: An optional name prefix to give our threads.
            worker_factory: The factory class to create worker threads.
            context: The context to pass to worker threads.
            idle_timeout: The timeout in seconds to wait for a new task.

        """
        if max_workers is None:
            # VXExecutor is often used to:
            # * CPU bound task which releases GIL
            # * I/O bound task (which releases GIL, of course)
            #
            # We use cpu_count + 4 for both types of tasks.
            # But we limit it to 32 to avoid consuming surprisingly large resource
            # on many core machine.
            max_workers = min(32, (os.cpu_count() or 1) + 4)
        if max_workers <= 0:
            raise ValueError("max_workers must be greater than 0")

        self._max_regular_workers = 1 if max_workers <= 4 else 2
        self._max_parttime_workers = max(max_workers - self._max_regular_workers, 0)

        self._thread_name_prefix = thread_name_prefix or self.__class__.__name__
        self._context = context
        self._work_queue: VXSchedTaskQueue = VXSchedTaskQueue()
        self._worker_factory = worker_factory

        self._idle_semaphore = threading.Semaphore(0)
        self._idle_timeout = idle_timeout

        self._shutdown = False
        self._shutdown_lock = threading.Lock()

        self._regular_workers: Set[threading.Thread] = set()
        self._parttime_workers: Set[threading.Thread] = set()

    def _adjust_workers(self) -> None:
        # 调整工作线程
        if self._idle_semaphore.acquire(blocking=False):
            return

        if len(self._regular_workers) < self._max_regular_workers:
            thread_name = (
                f"{self._thread_name_prefix or self}[r{self.__class__._counter()}]"
            )
            t = self._worker_factory(
                self._work_queue,  # type: ignore[arg-type]
                self._idle_semaphore,
                self._context,
                name=thread_name,
                idle_timeout=None,
            )
            t.start()
            self._regular_workers.add(t)
            return

        self._parttime_workers = {t for t in self._parttime_workers if t.is_alive()}
        num_threads = len(self._parttime_workers)
        if num_threads < self._max_parttime_workers:
            thread_name = (
                f"{self._thread_name_prefix or self}[p{self.__class__._counter()}]"
            )
            t = self._worker_factory(
                self._work_queue,  # type: ignore[arg-type]
                self._idle_semaphore,
                self._context,
                name=thread_name,
                idle_timeout=self._idle_timeout,
            )
            t.start()
            self._parttime_workers.add(t)

    def shutdown(self, wait: bool = True, *, cancel_futures: bool = False) -> None:
        with self._shutdown_lock:
            self._shutdown = True
            if cancel_futures:
                # Drain all work items from the queue, and then cancel their
                # associated futures.
                while not self._work_queue.empty():
                    try:
                        work_item = self._work_queue.get_nowait()
                        if work_item is None:
                            break
                        elif isinstance(work_item, VXTaskItem):
                            work_item.future.cancel()
                    except queue.Empty:
                        break

            # Send a wake-up to prevent threads calling
            # _work_queue.get(block=True) from permanently blocking.
            for t in itertools.chain(self._regular_workers, self._parttime_workers):
                self._work_queue.put(None)
        if wait:
            for t in itertools.chain(self._regular_workers, self._parttime_workers):
                if t.is_alive():
                    t.join()

    def apply(
        self, task: VXTaskItem, *, trigger: Optional[VXTrigger] = None
    ) -> Future[Any]:
        """提交任务

        Arguments:
            task {VXTaskItem} -- 提交的任务

        Returns:
            Future[Any] -- 返回任务的 Future
        """

        self._work_queue.put(task, trigger=trigger)
        self._adjust_workers()
        return task.future

    def submit(
        self, fn: Callable[..., Any], /, *args: Any, **kwargs: Any
    ) -> Future[Any]:
        """提交任务

        Arguments:
            task {VXTaskItem} -- 提交的任务

        Returns:
            Future[Any] -- 返回任务的 Future
        """
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError("cannot schedule new futures after shutdown")

            task = VXTaskItem(fn, *args, **kwargs)
            return self.apply(task)

    def delay(
        self,
        fu: Callable[[Any], Any],
        *args: Any,
        delay_time: float = 0,
        **kwargs: Any,
    ) -> Future[Any]:
        """延迟提交任务

        Arguments:
            task {VXTaskItem} -- 提交的任务
            trigger {VXTrigger} -- 触发器

        Returns:
            Future[Any] -- 返回任务的 Future
        """
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError("cannot schedule new futures after shutdown")
            delay_time = max(delay_time, 0)
            trigger = VXTrigger.once(datetime.now() + timedelta(seconds=delay_time))
            task = VXTaskItem(fu, *args, **kwargs)
            return self.apply(task, trigger=trigger)

    def __enter__(self) -> "VXSchedExecutor":
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException],  # type: ignore[override]
        exc_val: BaseException,  # type: ignore[override]
        exc_tb: Any,
    ) -> Literal[False]:
        self.shutdown(wait=True)
        return False


class async_task:
    """
    多线程提交任务
    example::

        @async_task
        def test():
            time.sleep(1)
    """

    __executor__ = VXSchedExecutor(thread_name_prefix="async_task", idle_timeout=600)

    def __init__(
        self,
        max_workers: int = 5,
        on_error: Literal["logging", "raise", "ignore"] = "raise",
    ) -> None:
        self._semaphore = threading.Semaphore(max_workers)
        self._on_error = on_error

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        def semaphore_func(*args: Any, **kwargs: Any) -> Any:
            with self._semaphore:
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    if self._on_error == "logging":
                        logging.error(
                            "async_task error: %s",
                            err,
                            exc_info=True,
                            stack_info=True,
                        )
                    elif self._on_error == "raise":
                        raise err from err
                    return None

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Future[Any]:
            return self.__executor__.submit(semaphore_func, *args, **kwargs)

        return wrapper


def async_map(
    func: Callable[..., Any],
    *iterables: Any,
    timeout: Optional[float] = None,
    chunsize: int = 1,
) -> Any:
    """异步map提交任务

    Arguments:
        func {Callable[..., Any]} -- 运行func

    Returns:
        Any -- 返回值
    """
    return async_task.__executor__.map(
        func, *iterables, timeout=timeout, chunksize=chunsize
    )


def run_every(
    func: Callable[[Any], Any],
    interval: float,
    *args: Any,
    start_dt: Optional[datetime] = None,
    end_dt: Optional[datetime] = None,
    **kwargs: Any,
) -> None:
    """每隔一段时间运行任务

    Arguments:
        func {Callable[..., Any]} -- 运行func
        interval {float} -- 时间间隔

    Keyword Arguments:
        start_dt {Optional[datetime]} -- 开始时间 (default: {None})
        end_dt {Optional[datetime]} -- 结束时间 (default: {None})
    """
    trigger = VXTrigger.every(interval, start_dt=start_dt, end_dt=end_dt)
    task = VXTaskItem(func, *args, **kwargs)
    async_task.__executor__.apply(
        task,
        trigger=trigger,
    )


if __name__ == "__main__":
    from vxutils import loggerConfig, timer

    loggerConfig("INFO", force=True)
    logging.warning("=====")
    start = time.perf_counter()
    pool = VXSchedExecutor(5, "hello_world")

    @async_task(on_error="raise")
    def test(i: int) -> str:
        time.sleep(0.1 * i)
        logging.warning(f"task {i} start")
        raise ValueError(f"task {i} error")
        # return f"{i + 1} done"

    with timer("test 12345", warnning=0.01):
        r = [test(i) for i in range(10)]
        print(r)
        print(time.perf_counter() - start)
        # print([i.result() for i in r])

    run_every(test, 1, 2)
    logging.info("=====")
    time.sleep(10)
    pool.shutdown(wait=True)
    logging.info("=====")
