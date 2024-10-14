from sais.notify import EnvVarCredentialsProvider
from sais.notify.clients.notify_client import NotifyClient
from sais.notify.config.const import ENDPOINT
from sais.notify.model.keepalive_model import KeepAliveModel


class KeepAliveHandler(object):
    def __init__(self, auth_provider: EnvVarCredentialsProvider):
        self.auth_provider = auth_provider

    def send_keep_alive(self, redis_key: str, redis_value: str, ttl_secs: int):
        client = NotifyClient(ENDPOINT, self.auth_provider)
        model = KeepAliveModel(
            redisKey=redis_key,
            redisValue=redis_value,
            ttlSecs=ttl_secs
        )
        return client.send_keep_alive(model)
