import logging
from queue import Queue

from PyQt5.QtCore import QThread, pyqtSlot, QObject, pyqtSignal

from esi.esi_core import EsiCore


class EsiQuery:

    def __init__(self, esi_core: EsiCore):
        self.esi_core = esi_core
        self.response = None

    def get_character_public_information(self, char_id):
        character_op = self.esi_core.app.op['get_characters_character_id'](
            character_id=char_id
        )
        return self.esi_core.client.request(character_op).data.name


class AsyncCharacterQueries(QObject):

    notify_update = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, shared_queue: Queue, shared_dict: dict):
        QObject.__init__(self)

        self.esi_core = None
        self.query_engine = None
        self.query_list = shared_queue
        self.shared_dict = shared_dict

        self.objThread = QThread()

        self.running = True
        # self.setDaemon(True)

    @pyqtSlot()
    def work(self) -> None:
        """

        :return:
        """
        logging.info("Character query service started.")

        self.esi_core = EsiCore()
        self.query_engine = EsiQuery(self.esi_core)

        try:
            while self.running:
                char_id = self.query_list.get(block=True)

                response = self.query_engine.get_character_public_information(char_id)
                self.shared_dict[char_id] = response
                self.notify_update.emit()
        finally:
            logging.warning("Character name query service terminated.")

    @pyqtSlot()
    def exit(self):
        logging.info("Character query service has exited.")

    def start(self):
        """
        Convenience function starting the thread for the ASync character name service
        :return:
        """
        self.moveToThread(self.objThread)
        self.finished.connect(self.objThread.quit)
        self.objThread.started.connect(self.work)
        self.objThread.finished.connect(self.exit)
        self.objThread.setObjectName("AsyncCharacterThread")
        self.objThread.start()

    def abort(self):
        self.sig_msg.emit('Worker #{} notified to abort'.format(self.__id))
        self.__abort = True
