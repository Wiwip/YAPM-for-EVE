# Using EsiApp [recommended]
from esipy import EsiApp
from esipy import EsiClient


class EsiCore:

    def __init__(self):
        self.esi_app = EsiApp()
        self.app = self.esi_app.get_latest_swagger

        self.client = EsiClient(
            retry_requests=True,  # set to retry on http 5xx error (default False)
            headers={'User-Agent': 'Something CCP can use to contact you and that define your app'},
            raw_body_only=False,  # default False, set to True to never parse response and only return raw JSON string content.
        )
