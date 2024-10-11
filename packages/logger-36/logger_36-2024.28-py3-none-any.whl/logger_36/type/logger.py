"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2023
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import logging as lggg
import sys as sstm
import traceback as tcbk
import types as t
import typing as h
from datetime import datetime as dttm
from pathlib import Path as path_t
from traceback import TracebackException as traceback_t

from logger_36.config.issue import ISSUE_CONTEXT_END, ISSUE_CONTEXT_SEPARATOR
from logger_36.config.message import DATE_FORMAT
from logger_36.constant.generic import NOT_PASSED
from logger_36.constant.issue import ISSUE_LEVEL_SEPARATOR, ORDER, order_h
from logger_36.constant.logger import (
    HIDE_WHERE_KWARG,
    LOGGER_NAME,
    WARNING_LOGGER_NAME,
    WARNING_TYPE_COMPILED_PATTERN,
    logger_handle_h,
)
from logger_36.constant.memory import UNKNOWN_MEMORY_USAGE
from logger_36.constant.message import expected_op_h
from logger_36.constant.record import SHOW_MEMORY_ATTR, SHOW_W_RULE_ATTR
from logger_36.task.format.memory import (
    FormattedUsageWithAutoUnit as FormattedMemoryUsage,
)
from logger_36.task.format.message import FormattedMessage
from logger_36.task.measure.chronos import ElapsedTime
from logger_36.task.measure.memory import CurrentUsage as CurrentMemoryUsage
from logger_36.type.issue import NewIssue, issue_t


@d.dataclass(slots=True, repr=False, eq=False)
class logger_t(lggg.Logger):
    name_: d.InitVar[str] = LOGGER_NAME
    level_: d.InitVar[int] = lggg.NOTSET
    activate_wrn_interceptions: d.InitVar[bool] = True

    # Must not be False until at least one handler has been added.
    should_hold_messages: bool = True
    exit_on_error: bool = False  # Implies exit_on_critical.
    exit_on_critical: bool = False

    on_hold: list[lggg.LogRecord] = d.field(init=False, default_factory=list)
    events: dict[int, int] = d.field(init=False, default_factory=dict)
    last_message_date: str = d.field(init=False, default="")
    any_handler_shows_memory: bool = d.field(init=False, default=False)
    memory_usages: list[tuple[str, int]] = d.field(init=False, default_factory=list)
    context_levels: list[str] = d.field(init=False, default_factory=list)
    staged_issues: list[issue_t] = d.field(init=False, default_factory=list)
    intercepted_wrn_handle: logger_handle_h | None = d.field(init=False, default=None)
    intercepted_log_handles: dict[str, logger_handle_h] = d.field(
        init=False, default_factory=dict
    )

    def __post_init__(
        self, name_: str, level_: int, activate_wrn_interceptions: bool
    ) -> None:
        """"""
        lggg.Logger.__init__(self, name_)
        self.setLevel(level_)
        self.propagate = False  # Part of lggg.Logger.

        for level in lggg.getLevelNamesMapping().values():
            self.events[level] = 0

        if activate_wrn_interceptions:
            self._ActivateWarningInterceptions()
        if self.exit_on_error:
            self.exit_on_critical = True

    def ResetEventCounts(self) -> None:
        """"""
        for level in self.events:
            self.events[level] = 0

    def _ActivateWarningInterceptions(self) -> None:
        """
        The log message will not appear if called from __post_init__ since there are no
        handlers yet.
        """
        if self.intercepted_wrn_handle is None:
            logger = lggg.getLogger(WARNING_LOGGER_NAME)
            self.intercepted_wrn_handle = logger.handle
            logger.handle = t.MethodType(_HandleForWarnings(self), logger)

            lggg.captureWarnings(True)
            self.info("Warning Interception: ON", **HIDE_WHERE_KWARG)

    def _DeactivateWarningInterceptions(self) -> None:
        """"""
        if self.intercepted_wrn_handle is not None:
            logger = lggg.getLogger(WARNING_LOGGER_NAME)
            logger.handle = self.intercepted_wrn_handle
            self.intercepted_wrn_handle = None

            lggg.captureWarnings(False)
            self.info("Warning Interception: OFF", **HIDE_WHERE_KWARG)

    def ToggleWarningInterceptions(self, state: bool, /) -> None:
        """"""
        if state:
            self._ActivateWarningInterceptions()
        else:
            self._DeactivateWarningInterceptions()

    def ToggleLogInterceptions(self, state: bool, /) -> None:
        """"""
        if state:
            self.ToggleLogInterceptions(False)

            all_loggers = [lggg.getLogger()] + [
                lggg.getLogger(_nme)
                for _nme in self.manager.loggerDict
                if _nme not in (self.name, WARNING_LOGGER_NAME)
            ]
            for logger in all_loggers:
                self.intercepted_log_handles[logger.name] = logger.handle
                logger.handle = t.MethodType(
                    _HandleForInterceptions(logger, self), logger
                )

            intercepted = sorted(self.intercepted_log_handles.keys())
            if intercepted.__len__() > 0:
                as_str = ", ".join(intercepted)
                self.info(
                    f"Now Intercepting LOGs from: {as_str}",
                    **HIDE_WHERE_KWARG,
                )
        elif self.intercepted_log_handles.__len__() > 0:
            for name, handle in self.intercepted_log_handles.items():
                logger = lggg.getLogger(name)
                logger.handle = handle
            self.intercepted_log_handles.clear()
            self.info("Log Interception: OFF", **HIDE_WHERE_KWARG)

    @property
    def max_memory_usage(self) -> int:
        """"""
        if self.memory_usages.__len__() > 0:
            return max(tuple(zip(*self.memory_usages))[1])
        return UNKNOWN_MEMORY_USAGE

    @property
    def max_memory_usage_full(self) -> tuple[str, int]:
        """"""
        if self.memory_usages.__len__() > 0:
            where_s, usages = zip(*self.memory_usages)
            max_usage = max(usages)

            return where_s[usages.index(max_usage)], max_usage

        return "?", UNKNOWN_MEMORY_USAGE

    def AddHandler(self, handler: lggg.Handler, should_hold_messages: bool, /) -> None:
        """"""
        self.should_hold_messages = should_hold_messages
        lggg.Logger.addHandler(self, handler)

        extension = getattr(handler, "extension", None)
        if extension is None:
            show_memory_usage = False
        else:
            show_memory_usage = getattr(extension, SHOW_MEMORY_ATTR, False)
        if show_memory_usage:
            self.any_handler_shows_memory = True

        extension = getattr(handler, "extension", handler.name)
        if isinstance(extension, str):
            name = extension
        else:
            name = getattr(extension, "name", "Anonymous")
        self.info(
            f'New handler "{name}" with class "{type(handler).__name__}" and '
            f"level {lggg.getLevelName(handler.level)}",
            **HIDE_WHERE_KWARG,
        )

    def handle(self, record: lggg.LogRecord, /) -> None:
        """"""
        if (not self.should_hold_messages) and (self.on_hold.__len__() > 0):
            for hold in self.on_hold:
                lggg.Logger.handle(self, hold)
            self.on_hold.clear()

        record.elapsed_time = ElapsedTime()

        if self.any_handler_shows_memory or not self.hasHandlers():
            # Memory usage is also added if there are no handlers yet, just in case.
            usage = CurrentMemoryUsage()
            self.memory_usages.append(
                (f"{record.module}.{record.funcName}.{record.lineno}", usage)
            )

            value, unit = FormattedMemoryUsage(usage, 1)
            record.memory_usage = f"{value}{unit}"

        date = dttm.now().strftime(DATE_FORMAT)
        if date != self.last_message_date:
            self.last_message_date = date
            # levelno: Added for management by logging.Logger.handle.
            date_record = lggg.makeLogRecord(
                {
                    "name": self.name,
                    "levelno": lggg.INFO,
                    "msg": f"DATE: {date}",
                    SHOW_W_RULE_ATTR: True,
                }
            )
            if self.should_hold_messages:
                self.on_hold.append(date_record)
            else:
                lggg.Logger.handle(self, date_record)

        if self.should_hold_messages:
            self.on_hold.append(record)
        else:
            lggg.Logger.handle(self, record)

        self.events[record.levelno] += 1
        if (self.exit_on_critical and (record.levelno is lggg.CRITICAL)) or (
            self.exit_on_error and (record.levelno is lggg.ERROR)
        ):
            # Also works if self.exit_on_error and record.levelno is lggg.CRITICAL since
            # __post_init__ set self.exit_on_critical if self.exit_on_error.
            sstm.exit(1)

    def Log(
        self,
        message: str,
        /,
        *,
        level: int | str = lggg.ERROR,
        actual: h.Any = NOT_PASSED,
        expected: h.Any | None = None,
        expected_is_choices: bool = False,
        expected_op: expected_op_h = "=",
        with_final_dot: bool = True,
    ) -> None:
        """"""
        if isinstance(level, str):
            level = lggg.getLevelNamesMapping()[level.upper()]
        message = FormattedMessage(
            message,
            actual=actual,
            expected=expected,
            expected_is_choices=expected_is_choices,
            expected_op=expected_op,
            with_final_dot=with_final_dot,
        )
        self.log(level, message)

    def LogException(
        self,
        exception: Exception,
        /,
        *,
        level: int | str = lggg.ERROR,
        should_remove_caller: bool = False,
    ) -> None:
        """"""
        if isinstance(level, str):
            level = lggg.getLevelNamesMapping()[level.upper()]
        lines = tcbk.format_exception(exception)
        if should_remove_caller:
            message = "\n".join(lines[:1] + lines[2:])
        else:
            # TODO: Explain:
            #     - Why it's not: "\n".join(lines)?
            #     - Why adding exception name here and not when removing caller?
            formatted = "".join(lines)
            message = f"{type(exception).__name__}:\n{formatted}"
        self.log(level, message)

    def ShowMessage(self, message: str, /, *, indented: bool = False) -> None:
        """
        See documentation of
        logger_36.catalog.handler.generic.generic_handler_t.ShowMessage.
        """
        for handler in self.handlers:
            ShowMessage = getattr(handler, "ShowMessage", None)
            if ShowMessage is not None:
                ShowMessage(message, indented=indented)

    def DisplayRule(self, /, *, text: str | None = None, color: str = "white") -> None:
        """"""
        for handler in self.handlers:
            DisplayRule = getattr(handler, "DisplayRule", None)
            if DisplayRule is not None:
                DisplayRule(text=text, color=color)

    def AddContextLevel(self, new_level: str, /) -> None:
        """"""
        self.context_levels.append(new_level)

    def AddedContextLevel(self, new_level: str, /) -> h.Self:
        """
        Meant to be used as:
        with self.AddedContextLevel("new level"):
            ...
        """
        self.AddContextLevel(new_level)
        return self

    def StageIssue(
        self,
        message: str,
        /,
        *,
        level: int = lggg.ERROR,
        actual: h.Any = NOT_PASSED,
        expected: h.Any | None = None,
        expected_is_choices: bool = False,
        expected_op: expected_op_h = "=",
        with_final_dot: bool = False,
    ) -> None:
        """"""
        context = ISSUE_CONTEXT_SEPARATOR.join(self.context_levels)
        issue = NewIssue(
            context,
            ISSUE_CONTEXT_END,
            message,
            level=level,
            actual=actual,
            expected=expected,
            expected_is_choices=expected_is_choices,
            expected_op=expected_op,
            with_final_dot=with_final_dot,
        )
        self.staged_issues.append(issue)

    @property
    def has_staged_issues(self) -> bool:
        """"""
        return self.staged_issues.__len__() > 0

    def CommitIssues(
        self,
        /,
        *,
        order: order_h = "when",
        unified: bool = False,
    ) -> None:
        """
        Note that issues after an issue with a level triggering process exit will not be
        logged.
        """
        if not self.has_staged_issues:
            return

        if order not in ORDER:
            raise ValueError(
                FormattedMessage(
                    "Invalid commit order",
                    actual=order,
                    expected=f"One of {str(ORDER)[1:-1]}",
                )
            )

        if order == "when":
            issues = self.staged_issues
        else:  # order == "context"
            issues = sorted(self.staged_issues, key=lambda _elm: _elm.context)
        """
        Format issues as an exception:
        try:
            raise ValueError("\n" + "\n".join(issues))
        except ValueError as exception:
            lines = ["Traceback (most recent call last):"] + tcbk.format_stack()[:-1]
            lines[-1] = lines[-1][:-1]
            lines.extend(tcbk.format_exception_only(exception))
            formatted = "\n".join(lines)
        """

        if unified:
            level, _ = issues[0].split(ISSUE_LEVEL_SEPARATOR, maxsplit=1)
            wo_level = []
            for issue in issues:
                _, issue = issue.split(ISSUE_LEVEL_SEPARATOR, maxsplit=1)
                wo_level.append(issue)
            self.log(int(level), "\n".join(wo_level), stacklevel=2)
        else:
            for issue in issues:
                level, issue = issue.split(ISSUE_LEVEL_SEPARATOR, maxsplit=1)
                self.log(int(level), issue, stacklevel=2)
        self.staged_issues.clear()

    def __enter__(self) -> None:
        """"""
        pass

    def __exit__(
        self,
        exc_type: Exception | None,
        exc_value: str | None,
        traceback: traceback_t | None,
        /,
    ) -> bool:
        """"""
        _ = self.context_levels.pop()
        return False


def _HandleForWarnings(interceptor: lggg.Logger, /) -> logger_handle_h:
    """"""

    def handle_p(_: lggg.Logger, record: lggg.LogRecord, /) -> None:
        pieces = WARNING_TYPE_COMPILED_PATTERN.match(record.msg)
        if pieces is None:
            # The warning message does not follow the default format.
            interceptor.handle(record)
            return

        GetPiece = pieces.group
        path = GetPiece(1)
        line = GetPiece(2)
        kind = GetPiece(3)
        message = GetPiece(4)

        duplicate = lggg.makeLogRecord(record.__dict__)
        duplicate.msg = f"{kind}: {message}"
        duplicate.pathname = path
        duplicate.module = path_t(path).stem
        duplicate.funcName = "?"
        duplicate.lineno = line

        interceptor.handle(duplicate)

    return handle_p


def _HandleForInterceptions(
    intercepted: lggg.Logger, interceptor: lggg.Logger, /
) -> logger_handle_h:
    """"""

    def handle_p(_: lggg.Logger, record: lggg.LogRecord, /) -> None:
        duplicate = lggg.makeLogRecord(record.__dict__)
        duplicate.msg = f"{record.msg} :{intercepted.name}:"
        interceptor.handle(duplicate)

    return handle_p


"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
