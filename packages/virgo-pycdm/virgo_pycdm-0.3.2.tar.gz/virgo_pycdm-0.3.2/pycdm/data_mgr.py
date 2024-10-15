import queue
import logging
from threading import Thread

import zmq.error

from .comm import ZmqAsyncConn

log = logging.getLogger(__name__)


class MsgReg:

    def __init__(self, i):
        self._q = queue.Queue()
        self._id = i

    def id_match(self, i: str):
        return self._id == i[0:len(self._id)]

    def add_msg(self, msg):
        self._q.put(msg)

    def get_msg(self):
        return self._q.get(block=True)


class DataManager:

    def __init__(self, addr):
        self._cdm_async = ZmqAsyncConn(addr)

        self._thread = Thread(target=self._frame_reader)
        self._thread.start()

        self._msg_reg = []

    def close(self):
        log.info("Closing DataManager")
        self._cdm_async.disconnect()
        self._thread.join()

    def register(self, s):
        reg = MsgReg(s)
        self._msg_reg.append(reg)
        return reg

    def _frame_reader(self):
        log.info("FRAME READER STARTED")
        try:
            while True:
                msg_id = self._cdm_async.recv().decode()
                msg = self._cdm_async.recv()
                for i in self._msg_reg:
                    if i.id_match(msg_id):
                        i.add_msg(msg)
        except zmq.error.ContextTerminated:
            log.warning("Exiting from frame reader")

