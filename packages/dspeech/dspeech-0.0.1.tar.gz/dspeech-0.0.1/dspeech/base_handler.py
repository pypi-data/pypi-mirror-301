# Raw code from https://github.com/huggingface/speech-to-speech
# Please refer to https://github.com/huggingface/speech-to-speech
# for more details.

# modified by zhaosheng@nuaa.edu.cn
# 2024-09-24

from time import perf_counter
import logging

logger = logging.getLogger(__name__)


class BaseHandler:
    """
    Base class for pipeline parts. Each part of the pipeline has an input and an output queue.
    The `setup` method along with `setup_args` and `setup_kwargs` can be used to address the specific requirements of the implemented pipeline part.
    To stop a handler properly, set the stop_event and, to avoid queue deadlocks, place b"END" in the input queue.
    Objects placed in the input queue will be processed by the `process` method, and the yielded results will be placed in the output queue.
    The cleanup method handles stopping the handler, and b"END" is placed in the output queue.
    """

    def __init__(self, setup_args=(), setup_kwargs={}):

        self.setup(*setup_args, **setup_kwargs)

    def setup(self):
        pass
