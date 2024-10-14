"""scheduler module"""

import signal
from importlib import machinery, util
import logging
import os
import time
import uuid
import json
from pathlib import Path
from argparse import ArgumentParser, Namespace
from typing import Any, List, Optional, Dict, Callable, Union
import threading
import signal
from concurrent.futures import Future
from pydantic import Field
from vxutils import VXJSONEncoder, to_json
from vxutils.context import VXContext
from vxutils.logger import loggerConfig
from vxutils.executor import VXTaskItem, async_task, VXTrigger
from vxutils.datamodel.core import VXDataModel


ON_INIT_EVENT = "__init__"
ON_REPLY_EVENT = "__reply__"
ON_TASK_COMPLETE_EVENT = "__task_complete__"
ON_EXIT_EVENT = "__exit__"


class VXEvent(VXDataModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    type: str = ""
    data: Dict[str, Any] = Field(default_factory=dict, frozen=True)
    priority: int = 10
    channel: str = "default"
    reply_to: str = ""

    def __lt__(self, other: "VXEvent") -> bool:
        return (-self.priority, hash(id)) < (-other.priority, hash(other.id))


__handlers__: Dict[str, List[Callable[[VXContext, VXEvent], Any]]] = {}


def register_handler(
    event_type: str,
) -> Callable[[Callable[[VXContext, VXEvent], Any]], Any]:
    """注册事件处理函数

    Arguments:
        event_type {str} -- 事件类型

    Returns:
        Callable[[Callable[[VXContext, VXEvent], Any]], None] -- 事件处理函数
    """
    global __handlers__
    if event_type not in __handlers__:
        __handlers__[event_type] = []

    def wrapper(
        handler: Callable[[VXContext, VXEvent], Any],
    ) -> Callable[[VXContext, VXEvent], Any]:
        __handlers__[event_type].append(handler)
        logging.warning(f"Register event handler: {event_type} -> {handler}")
        return handler

    return wrapper


def unregister_handler(
    event_type: str, handler: Optional[Callable[[VXContext, VXEvent], Any]] = None
) -> None:
    """注销事件处理函数

    Arguments:
        event_type {str} -- 事件类型

    Keyword Arguments:
        handler {Optional[Callable[[VXContext, VXEvent], Any]]} -- 事件处理函数 (default: {None})
    """
    global __handlers__
    if not handler:
        __handlers__.pop(event_type, [])
    elif handler in __handlers__[event_type]:
        __handlers__[event_type].remove(handler)
        logging.warning(f"Unregister event handler: {event_type} -> {handler}")


__default_config__: Dict[str, Any] = {
    "daily": {"on_settle": {"timestr": "00:00:00"}},
    "every": {"on_second": {"interval": 1}},
}
__context__: VXContext = VXContext()
__ACTIVE__: bool = True


def _handle_event(context: VXContext, event: VXEvent) -> None:
    global __handlers__
    handlers = __handlers__.get(event.type, [])
    if len(handlers) == 1:
        handler = handlers[0]
        try:
            handler(context, event)
        except Exception as err:
            logging.error(
                f"Event handler error: {event.type} -> {handler}", exc_info=True
            )
    else:
        for handler in handlers:
            task = VXTaskItem(handler, context, event)
            async_task.__executor__.apply(task)


class VXPublisher:
    def __init__(
        self,
        context: VXContext = __context__,
        apply_method: Optional[
            Callable[[VXTaskItem, Optional[VXTrigger]], Future[Any]]
        ] = None,
    ) -> None:
        self.context = context
        self.apply_method = (
            apply_method if apply_method is not None else async_task.__executor__.apply
        )

    def __call__(
        self,
        event: Union[str, VXEvent],
        *,
        trigger: Optional[VXTrigger] = None,
        data: Optional[Dict[str, Any]] = None,
        channel: str = "default",
        priority: int = 10,
        reply_to: str = "",
    ) -> Future[Any]:
        if isinstance(event, str):
            event = VXEvent(
                type=event,
                data=data or {},
                channel=channel,
                priority=priority,
                reply_to=reply_to,
            )
        task = VXTaskItem(_handle_event, self.context, event=event)
        return self.apply_method(task=task, trigger=trigger)  # type: ignore[no-any-return, operator]


publish = VXPublisher()


def load_modules(mod_path: Union[str, Path]) -> Any:
    """加载策略目录"""
    if not os.path.exists(mod_path):
        logging.warning(msg=f"{mod_path} is not exists")
        return

    modules = os.listdir(mod_path)
    logging.info(f"loading strategy dir: {mod_path}.")
    logging.info("=" * 80)
    for mod in modules:
        if (not mod.startswith("__")) and mod.endswith(".py"):
            try:
                loader = machinery.SourceFileLoader(mod, os.path.join(mod_path, mod))
                spec = util.spec_from_loader(loader.name, loader)
                if spec is None:
                    logging.error(f"Load Module: {mod} Failed.")
                    continue

                strategy_mod = util.module_from_spec(spec)
                loader.exec_module(strategy_mod)
                logging.info(f"Load Module: {strategy_mod} Sucess.")
                logging.info("+" * 80)
            except Exception as err:
                logging.error(f"Load Module: {mod} Failed. {err}", exc_info=True)
                logging.error("-" * 80)


def quit_handler(signum: int, frame: Any) -> None:
    global __context__
    logging.warning("========== Scheduler 开始执行退出任务... ==========")

    try:
        with open("data/params.json", "w") as f:
            json.dump(__context__.params, f, indent=4, cls=VXJSONEncoder)
            logging.info("保存参数至: %s", Path("data/params.json").absolute())
            logging.debug("保存参数: %s", to_json(__context__.params))
    except Exception as err:
        logging.error("保存参数失败: %s", err)

    finally:
        if ON_EXIT_EVENT in __handlers__:
            publish(ON_EXIT_EVENT)
        async_task.__executor__.shutdown(wait=True)
        logging.info("========== Scheduler 已停止运行... ==========")
        os._exit(0)


def shutdown() -> None:
    global __ACTIVE__
    __ACTIVE__ = False


def init(args: Namespace) -> None:
    loggerConfig(force=True)
    target = Path(args.target).absolute()
    logging.info("初始化模块: %s", target)

    for d in [
        "mod",
        "etc",
        "data",
        "log",
    ]:
        if (target / d).exists():
            logging.warning("目录已存在: %s", target / d)
        else:
            (target / d).mkdir(parents=True)
            logging.info("创建目录: %s", target / d)

    if not (target / "etc/default_config.json").exists():
        with open(target / "etc/default_config.json", "w") as f:
            json.dump(__default_config__, f, indent=4)
            logging.info("创建默认配置文件: %s", target / "etc/default_config.json")

    if not (target / "data/params.json").exists():
        with open(target / "data/params.json", "w") as f:
            json.dump({}, f, indent=4)
            logging.info("创建参数文件: %s", target / "data/params.json")


def run(args: Optional[Namespace] = None) -> None:
    global __context__, __handlers__, __ACTIVE__

    if args is None:
        args = Namespace(
            config="etc/config.json", mod="mod", log="log/message.log", verbose=False
        )

    log_level = "DEBUG" if args.verbose else "INFO"
    log_file = args.log if args.log else ""
    if args.log:
        log_file = Path(args.log).absolute()
        if log_file.is_dir():
            log_file = log_file / "vxsched.log"

        if not log_file.parent.exists():
            log_file.parent.mkdir(parents=True)

    loggerConfig(level=log_level, filename=log_file, force=True)
    logging.info("========== Scheduler 启动... ==========")

    # 加载模块
    configfile = Path(args.config)
    __context__.clear()
    __context__.config = {}
    try:
        with open(configfile, "r") as f:
            config = json.load(f)
    except BaseException as err:
        logging.warning("加载配置文件失败: %s", err)
        config = {}
    __context__.config.update(**config)
    logging.info("加载配置: %s", __context__.config)

    __context__.params = {}
    try:
        with open("data/params.json", "r") as f:
            params = json.load(f)
            __context__.params.update(**params)
    except BaseException as err:
        logging.warning("加载参数文件失败: %s", err)

    logging.info("加载参数: %s", __context__.params)

    mod = Path(args.mod)
    if not mod.parent.exists():
        mod.mkdir(parents=True, exist_ok=True)
    load_modules(mod_path=mod)

    try:
        if ON_INIT_EVENT in __handlers__:
            logging.info("========== Scheduler 开始执行初始化任务... ==========")
            fu = publish(ON_INIT_EVENT)
            fu.result(timeout=5)
        logging.info(
            "========== Scheduler 初始化完成... 按下 Ctrl+C 退出... =========="
        )
        __ACTIVE__ = True
        if threading.current_thread() is threading.main_thread():
            signal.signal(signal.SIGINT, quit_handler)
        while __ACTIVE__:
            time.sleep(1)
        quit_handler(signum=signal.SIGINT, frame=None)
    except KeyboardInterrupt:
        pass

    except Exception as err:
        logging.error("运行时错误...%s", err, exc_info=True)
        quit_handler(signum=signal.SIGINT, frame=None)


def main() -> None:
    parser = ArgumentParser(description="vxsched 事件驱动调度器")
    subparser = parser.add_subparsers(description="运行子命令")

    # 初始化模块
    init_parser = subparser.add_parser("init", help="初始化模块")
    init_parser.add_argument("target", type=str, default=".", help="目标目录")
    init_parser.set_defaults(func=init)

    # 运行策略模块
    run_parser = subparser.add_parser("run", help="运行模块")
    run_parser.add_argument(
        "-c", "--config", default="etc/config.json", help="配置文件"
    )
    run_parser.add_argument("-m", "--mod", default="mod", help="事件列表")
    run_parser.add_argument("-l", "--log", default="log/message.log", help="日志文件")
    run_parser.add_argument(
        "-v", "--verbose", default=False, help="调试模式", action="store_true"
    )
    run_parser.set_defaults(func=run)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
