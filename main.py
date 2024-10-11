import numpy as np

from API import API
from Killing import Killing
from view import View

import random
import json


class Solution:
    def __init__(self):
        self.api = None
        self.view = View()
        self.killing = Killing()

    def set_api(self, api):
        self.api = api

    def main_process(self):
        response = self.api.start()
        req_code = 200
        while req_code == 200:
            self.view.update(response)

            command_to_transports_kill = self.killing.try_to_kill(response["transports"],
                                                                  response["enemies"],
                                                                  response["attackRange"],
                                                                  response["attackExplosionRadius"],
                                                                  response["attackDamage"])
            print(command_to_transports_kill)

            move = self.base_movement(response["transports"], command_to_transports_kill)

            self.api.write_data_to_build(move)

            req_code, response = self.api.sendReqCommand()

            print('GAME')
            json_string = json.dumps(response, indent=4)
            # Print the JSON string to the console
            # print(json_string)

        ...

    def base_movement(self, _transports, command_to_transports_kill):
        transports = []

        ind = 0
        for transport in _transports:
            transports.append(
                {
                    "acceleration": {
                        "x": 2,
                        "y": 2
                    },
                    "activateShield": False,
                    "attack": {
                        "x": command_to_transports_kill[ind]['x'],
                        "y": command_to_transports_kill[ind]['y']
                    },
                    "id": transport["id"]
                }
            )
            ind += 1
        return {"transports": transports}


api = API()
sol = Solution()
sol.set_api(api)
sol.main_process()
