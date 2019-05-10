from esi.esi_core import EsiCore


class EsiCharacter:

    def __init__(self, esi_core: EsiCore, character_id):
        self.esi_core = esi_core
        self.character_id = character_id

        self.response = None
        self.get_character_public_information()

    def get_character_public_information(self):
        character_op = self.esi_core.app.op['get_characters_character_id'](
            character_id=self.character_id
        )
        self.response = self.esi_core.client.request(character_op)

    @property
    def name(self):
        return self.response.data.name

