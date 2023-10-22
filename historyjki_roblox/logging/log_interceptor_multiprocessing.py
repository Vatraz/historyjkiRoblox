from multiprocessing.managers import DictProxy

from historyjki_roblox.logging.log_interceptor import (
    LogInterceptionError,
    LogInterceptorBase,
)


class MultiprocessingLogInterceptor(LogInterceptorBase):
    def __init__(self, log_dict: DictProxy, process_status_key: str):
        self._log_dict = log_dict
        self._process_key = process_status_key

    def intercept(self, log: str, log_time: float):
        try:
            # str() because keywords must be strings in DictProxy :<
            log_update = {str(log_time): log}
            self._log_dict[self._process_key] = dict(
                self._log_dict[self._process_key], **log_update
            )
        except Exception as exe:
            raise LogInterceptionError(exe)
