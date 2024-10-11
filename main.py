import numpy as np

from API import API
from view import View

import random
import json


class Solution:
    def __init__(self):
        self.api = None
        self.view = View()

    def set_api(self, api):
        self.api = api

    def main_process(self):
        response = self.api.start()
        req_code = 200
        while req_code == 200:
            self.view.update(response)

            # 1) Надо решить, кого атаковать
            # 2) Стоит ли куда-то съебаться

            move = self.base_movement(response["transports"])

            self.api.write_data_to_build(move)

            req_code, response = self.api.sendReqCommand()



        ...

    def base_movement(self, _transports):
        transports = []

        for transport in _transports:
            transports.append(
                {
                    "acceleration": {
                        "x": 2,
                        "y": 2
                    },
                    "activateShield": False,
                    "attack": {
                        "x": 0,
                        "y": 0
                    },
                    "id": transport["id"]
                }
            )
        return {"transports": transports}



api = API()
sol = Solution()
sol.set_api(api)
sol.main_process()
