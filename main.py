import numpy as np
from API import API
import random
import json


class Solution:
    def __init__(self):
        self.api = None

    def set_api(self, api):
        self.api = api

    def main_process(self):
        response = self.api.start()

        # 1) Надо решить, кого атаковать
        # 2) Стоит ли куда-то съебаться

        response = self.api.sendReqCommand()


api = API()
sol = Solution()
sol.set_api(api)
sol.main_process()
