import numpy as np

from API import API
from NotWallDead import *
from Killing import Killing
from view import View

import random
import json

from multiprocessing import Process, Queue


class Solution:
    def __init__(self):
        self.api = None

        self.killing = Killing()

    def set_api(self, api):
        self.api = api

    def main_process(self, _que_view: Queue):
        response = self.api.start()
        req_code = 200
        while True:
            if req_code == 200:
                _que_view.put(response)

                command_to_transports_kill = self.killing.try_to_kill(response["transports"],
                                                                      response["enemies"],
                                                                      response["attackRange"],
                                                                      response["attackExplosionRadius"],
                                                                      response["attackDamage"])

                dir_to_move = []
                for transport in response["transports"]:
                    dir_to_move.append(transport['velocity'])

                wall_dangers = wall_checking(response["transports"],
                                             response["mapSize"])

                ind = 0
                for wall_danger in wall_dangers:
                    if wall_danger['wall_danger'] is True:
                        if wall_danger['x'] != 0:
                            dir_to_move[ind]['x'] = wall_danger['x']
                        if wall_danger['y'] != 0:
                            dir_to_move[ind]['y'] = wall_danger['y']
                        ind += 1

                transports = self.base_movement(response["transports"], command_to_transports_kill, dir_to_move)

                self.api.write_data(transports)
                req_code, response = self.api.sendReqCommand()

                # print('GAME')
                # json_string = json.dumps(response, indent=4)
                # Print the JSON string to the console
                # print(json_string)

            else:
                self.api.write_empty_data()
                req_code, response = self.api.sendReqCommand()

            ...

    def base_movement(self, _transports, command_to_transports_kill, dir_to_move):
        transports = []

        ind = 0
        for transport in _transports:
            transports.append(
                {
                    "acceleration": {
                        "x": dir_to_move[ind]['x'],
                        "y": dir_to_move[ind]['y']
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


def viewer_process(_que: Queue):
    view = View()

    while True:
        if _que.empty():
            continue

        info = _que.get()
        view.update(info)


if __name__ == '__main__':
    que_view = Queue()
    p = Process(target=viewer_process, args=(que_view,))
    p.start()

    api = API()
    sol = Solution()
    sol.set_api(api)
    sol.main_process(que_view)
