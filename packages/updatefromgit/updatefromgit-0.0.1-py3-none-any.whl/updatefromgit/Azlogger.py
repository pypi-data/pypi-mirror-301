import logging
from enum import Enum
from typing import Union

# Add a level that will always be shown.
# Used by group(), endgroup() and section()
ALWAYS = 100
logging.addLevelName(ALWAYS, "ALWAYS")


class AzFormattersEnum(Enum):
    logissue = logging.Formatter(
        "##vso[task.logissue type=%(az_type)s sourcepath=%(pathname)s linenumber=%(lineno)d]%(msg)s"  # noqa
    )
    logfmt = logging.Formatter("##[%(az_type)s]%(msg)s")
    default = logging.Formatter("%(msg)s")


class AzFormatter(logging.Formatter):
    def __init__(self):
        pass

    def format(self, record: logging.LogRecord) -> str:
        az_fmt = getattr(record, "az_fmt", None)

        if not isinstance(az_fmt, AzFormattersEnum):
            az_fmt = AzFormattersEnum.default
        elif not hasattr(record, "az_type"):
            setattr(record, "az_type", record.levelname.lower())

        return az_fmt.value.format(record)


class AzLogger(logging.LoggerAdapter):
    def __init__(self, obj: Union[logging.Logger, str]) -> None:
        if isinstance(obj, str):
            super().__init__(logging.getLogger(obj), {})
        elif isinstance(obj, logging.Logger):
            super().__init__(obj, {})
        handler = logging.StreamHandler()
        handler.setFormatter(AzFormatter())
        self.logger.addHandler(handler)
        self.stacklevel = 3

    def __inject_extra(self, params, **kwargs):
        extra = params.get("extra", {})
        extra.update(kwargs)
        params["extra"] = extra
        return params

    # see https://docs.python.org/3/library/logging.html#logging.Logger.findCaller # noqa
    def __increment_stacklevel(self, kwargs, inc: int = 1):
        kwargs["stacklevel"] = kwargs.get("stacklevel", self.stacklevel) + inc

    def process(self, msg, kwargs):
        kwargs = self.__inject_extra(kwargs, **self.extra)
        return msg, kwargs

    def issueerror(self, msg, *args, **kwargs):
        kwargs = self.__inject_extra(
            kwargs, az_fmt=AzFormattersEnum.logissue, az_type="error"
        )
        self.log(logging.ERROR, msg, *args, **kwargs)

    def issuewarning(self, msg, *args, **kwargs):
        kwargs = self.__inject_extra(
            kwargs, az_fmt=AzFormattersEnum.logissue, az_type="warning"
        )
        self.log(logging.WARNING, msg, *args, **kwargs)

    def section(self, msg, *args, **kwargs):
        kwargs = self.__inject_extra(
            kwargs, az_fmt=AzFormattersEnum.logfmt, az_type="section"
        )
        self.log(ALWAYS, msg, *args, **kwargs)

    def group(self, msg, *args, **kwargs):
        kwargs = self.__inject_extra(
            kwargs, az_fmt=AzFormattersEnum.logfmt, az_type="group"
        )
        self.log(ALWAYS, msg, *args, **kwargs)

    def endgroup(self, msg, *args, **kwargs):
        kwargs = self.__inject_extra(
            kwargs, az_fmt=AzFormattersEnum.logfmt, az_type="endgroup"
        )
        self.log(ALWAYS, msg, *args, **kwargs)

    def command(self, msg, *args, **kwargs):
        kwargs = self.__inject_extra(
            kwargs, az_fmt=AzFormattersEnum.logfmt, az_type="command"
        )
        self.log(logging.INFO, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        kwargs = self.__inject_extra(
            kwargs, az_fmt=AzFormattersEnum.logfmt, az_type="error"
        )
        self.log(logging.ERROR, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        kwargs = self.__inject_extra(
            kwargs, az_fmt=AzFormattersEnum.logfmt, az_type="warning"
        )
        self.log(logging.WARNING, msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self.__increment_stacklevel(kwargs)
        super().log(level, msg, *args, **kwargs)