import json
import logging
from http import HTTPStatus

import requests

from sais.notify.auth.auth_info import EnvVarCredentialsProvider
from sais.notify.config.const import LOGGER_NAME
from sais.notify.model.message_model import MessageModel
from sais.notify.model.keepalive_model import KeepAliveModel

logger = logging.getLogger(LOGGER_NAME)
logging.basicConfig(level=logging.INFO)


class NotifyClient(object):
    def __init__(self, endpoint, auth_provider: EnvVarCredentialsProvider):
        self.endpoint = endpoint
        self.auth_provider = auth_provider

    def send_notification(self, message_info: MessageModel) -> bool:
        headers = {
            'Authorization': self.auth_provider.token,
            'Content-Type': 'application/json'
        }
        response = requests.post(f'{self.endpoint}/api/notify/v1/notify/send', headers=headers,
                                 json=message_info.model_dump(by_alias=True, exclude_none=True))

        if response.status_code == HTTPStatus.OK:
            response_data = response.json()
            if response_data.get('msgCode') == '10000':
                logger.info(f'Notification sent type {message_info.type} to {message_info.to} successfully')
                return True
            else:
                logger.error(f'Error sending notification: {response.status_code} - {response.text}')
        else:
            logger.error(f'Error sending notification: {response.status_code}')
        return False

    def send_keep_alive(self, keep_alive_info: KeepAliveModel) -> bool:
        headers = {
            'Authorization': self.auth_provider.token,
            'Content-Type': 'application/json'
        }
        response = requests.post(f'{self.endpoint}/api/notify/v1/notify/keepalive', headers=headers,
                                 json=keep_alive_info.model_dump(by_alias=True, exclude_none=True))

        if response.status_code == HTTPStatus.OK:
            response_data = response.json()
            if response_data.get('msgCode') == '10000':
                logger.info(f'Keepalive sent key {keep_alive_info.redis_key} to redis successfully')
                return True
            else:
                logger.error(f'Error sending notification: {response.status_code} - {response.text}')
        else:
            logger.error(f'Error sending notification: {response.status_code}')
        return False
