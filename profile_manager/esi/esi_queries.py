import time
from queue import Queue
from threading import Thread
import logging

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


class AsyncCharacterQueries(Thread):

    def __init__(self, shared_queue: Queue, shared_dict: dict):
        Thread.__init__(self)

        self.esi_core = None
        self.query_engine = None
        self.query_list = shared_queue
        self.shared_dict = shared_dict
        self.running = True

    def run(self) -> None:
        logging.info("Character query service started.")
        self.esi_core = EsiCore()
        self.query_engine = EsiQuery(self.esi_core)
        time.sleep(10)

        try:
            while self.running:
                char_id = self.query_list.get(block=True)

                response = self.query_engine.get_character_public_information(char_id)
                self.shared_dict[char_id] = response
        finally:
            logging.warning("Character name query service terminated.")

