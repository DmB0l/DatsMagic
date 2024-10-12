import numpy as np

from API import API
from NotWallDead import *
from Killing import Killing
from view import View
from Moving import Moving

import random
import json

from multiprocessing import Process, Queue


class Solution:
    def __init__(self):
        self.api = None

        self.killing = Killing()
        self.moving = Moving()

    def activated_shields(self, transports):
        activating_shield = []
        for transport in transports:
            if transport['health'] < 100 and transport['shieldCooldownMs'] == 0:
                activating_shield.append(True)
            else:
                activating_shield.append(False)
        return activating_shield

    def set_api(self, api):
        self.api = api

    def main_process(self, _que_view: Queue):
        response = self.api.start()
        req_code = 200
        while True:
            if req_code == 200:
                _que_view.put(response)

                print(len(response["enemies"]))

                shields = self.activated_shields(response["transports"])

                command_to_transports_kill = self.killing.try_to_kill(response["transports"],
                                                                      response["enemies"],
                                                                      response["attackRange"],
                                                                      response["attackExplosionRadius"],
                                                                      response["attackDamage"])

                dir_to_move = []
                ind = 0
                for transport in response["transports"]:
                    # dir_to_move.append(transport['velocity'])
                    gold_coords = self.moving.best_way_to_bounties(transport, response['bounties'])
                    vec_move = self.moving.move(gold_coords['x'], gold_coords['y'],
                                                response["transports"][ind], response['maxAccel'])
                    dir_to_move.append(vec_move)
                    ind += 1

                anomaly_dangers = Moving.anomaly_dodge(response)
                for id_transport_rec, recommendation in anomaly_dangers.items():
                    ind = 0
                    for transport in response["transports"]:
                        if transport['id'] == id_transport_rec:
                            break
                        ind += 1
                    if recommendation['priority'] == 'HIGH':
                        vec_move = self.moving.move(recommendation['vector']['x'], recommendation['vector']['y'],
                                                    response["transports"][ind], response['maxAccel'])
                        dir_to_move[ind]['x'] = vec_move['x']
                        dir_to_move[ind]['y'] = vec_move['y']


                wall_dangers = wall_checking(response["transports"],
                                             response["mapSize"],
                                             response["maxAccel"])

                ind = 0
                for wall_danger in wall_dangers:
                    if wall_danger['wall_danger'] is True:
                        # print('wall_danger')
                        # print('ind: ' + str(ind))
                        # print('response[maxAccel]' + str(response["maxAccel"]))
                        # print(wall_danger)
                        # print(response["transports"][ind])
                        # if wall_danger['x'] != 0:
                        dir_to_move[ind]['x'] = wall_danger['x']
                        # if wall_danger['y'] != 0:
                        dir_to_move[ind]['y'] = wall_danger['y']
                    ind += 1

                transports = self.base_movement(response["transports"], command_to_transports_kill, dir_to_move, shields)

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

    def base_movement(self, _transports, command_to_transports_kill, dir_to_move, shields):
        transports = []

        ind = 0
        for transport in _transports:
            transports.append(
                {
                    "acceleration": {
                        "x": dir_to_move[ind]['x'],
                        "y": dir_to_move[ind]['y']
                    },
                    "activateShield": shields[ind],
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
