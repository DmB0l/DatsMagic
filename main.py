import numpy as np
from API import API
import random
import json


class Solution:
    def __init__(self):
        self.turn = -1
        self.api = None

    def set_api(self, api):
        self.api = api

    def main_process(self):
        self.api.start()
        while True:
            self.step(self.api.turn)

    def step(self, turn):
        # Первый ход, прошлое состояние известно
        if (turn is None) or (self.turn == turn):
            return

        api.clear_data_to_send()

        # 1) Надо решить, кого атаковать

        # 2) Стоит ли куда-то съебаться

        # 3) Надо решить, куда строить

        response = self.api.sendReqCommand()


api = API()
sol = Solution()
sol.set_api(api)
sol.main_process()
