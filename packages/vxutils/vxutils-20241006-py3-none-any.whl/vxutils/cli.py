"""命令行生成器"""

from argparse import ArgumentParser, _SubParsersAction, _FormatterClass, Action
from typing import Any, Callable, Optional, Sequence


class VXSubParser:
    def __init__(self, sub_parser: _SubParsersAction[ArgumentParser]) -> None:
        self._sub_parser = sub_parser

    def __call__(self, func: Callable[..., Any]) -> Any:
        pass


class VXArgumentParser(ArgumentParser):
    """命令行生成器"""

    def __init__(
        self,
        prog: Optional[str] = None,
        usage: Optional[str] = None,
        description: Optional[str] = None,
        epilog: Optional[str] = None,
        parents: Sequence[ArgumentParser] = [],
        formatter_class: Optional[_FormatterClass] = None,
        prefix_chars: str = "-",
        fromfile_prefix_chars: Optional[str] = None,
        argument_default: Any = None,
        conflict_handler: str = "error",
        add_help: bool = True,
        allow_abbrev: bool = True,
        exit_on_error: bool = True,
    ) -> None:
        self._parser = ArgumentParser(
            prog=prog,
            usage=usage,
            description=description,
            epilog=epilog,
            parents=parents,
            formatter_class=formatter_class,  # type: ignore[arg-type]
            prefix_chars=prefix_chars,
            fromfile_prefix_chars=fromfile_prefix_chars,
            argument_default=argument_default,
            conflict_handler=conflict_handler,
            add_help=add_help,
            allow_abbrev=allow_abbrev,
            exit_on_error=exit_on_error,
        )

    def add_command(
        self,
        *,
        title: str = "",
        description: str | None = None,
        prog: str = "",
        action: type[Action] = None,
        option_string: str = None,
        dest: str | None = None,
        required: bool = None,
        help: str | None = None,
        metavar: str | None = None,
    ) -> VXSubParser:
        sub_parser = self._parser.add_subparsers(
            title=title,
            description=description,
            prog=prog,
            action=action,
            option_string=option_string,
            dest=dest,
            required=required,
            help=help,
            metavar=metavar,
        )
        return VXSubParser(sub_parser)
