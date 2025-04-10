from ibind import IbkrClient
from ibind.oauth.oauth1a import OAuth1aConfig
from src.logging.logger import project_logger
from os import environ as env

_LOGGER = project_logger(f"{__name__}")

class IBKRConnection():

    def connect(self) -> None:

        _LOGGER.info("Connecting IBKR client")

        self.client = IbkrClient(
            use_oauth=True,
            oauth_config=OAuth1aConfig(
                access_token=env['IBIND_OAUTH1A_ACCESS_TOKEN'],
                access_token_secret=env['IBIND_OAUTH1A_ACCESS_TOKEN_SECRET'],
                consumer_key=env['IBIND_OAUTH1A_CONSUMER_KEY'],
                dh_prime=env['IBIND_OAUTH1A_DH_PRIME'],
                encryption_key_fp=env['IBIND_OAUTH1A_ENCRYPTION_KEY_FP'],
                signature_key_fp=env['IBIND_OAUTH1A_SIGNATURE_KEY_FP'],
        )
    )