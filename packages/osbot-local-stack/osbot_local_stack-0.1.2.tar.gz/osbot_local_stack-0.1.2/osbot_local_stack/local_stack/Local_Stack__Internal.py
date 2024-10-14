import requests
from osbot_utils.utils.Objects import dict_to_obj

from osbot_utils.utils.Http import url_join_safe

from osbot_utils.utils.Env import get_env

from osbot_utils.base_classes.Type_Safe import Type_Safe

ENV_NAME__LOCAL_STACK__TARGET_SERVER = 'LOCAL_STACK__TARGET_SERVER'
DEFAULT__LOCAL_STACK__TARGET_SERVER  = 'http://localhost:4566'

class Local_Stack__Internal(Type_Safe):

    def target_server(self):
        return get_env(ENV_NAME__LOCAL_STACK__TARGET_SERVER, DEFAULT__LOCAL_STACK__TARGET_SERVER)

    def internal__health(self):
        path  = '/_localstack/health'
        url = url_join_safe(self.target_server(), path)

        json_data = requests.get(url).json()
        obj_data = dict_to_obj(json_data)
        return obj_data