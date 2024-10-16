import time
from http.client import responses

import numpy as np

from API import API
from NotWallDead import *
from Killing import Killing
# from view import View
from Moving import Moving
from RewindClient import RewindClient

import random
import json

from multiprocessing import Process, Queue


class Solution:
    def __init__(self):
        self.api = None

        self.killing = Killing()
        self.moving = Moving()
        self.rewind_client = RewindClient()

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

    def main_process(self):
        response = api.read_log()
        print(str(response))
        ind = 0
        for transport in response[0]['transports']:
            print(str(transport))
            self.rewind_client.circle(transport['x'], transport['y'], 30, self.rewind_client.DARK_GREEN, fill=True)
            self.rewind_client.circle_popup(transport['x'], transport['y'], 30, "transport " + str(ind))
            ind += 1
        for anom in response[0]['anomalies']:
            print(str(anom))
            self.rewind_client.circle(anom['x'], anom['y'], anom['radius'], self.rewind_client.DARK_RED, fill=True)
            self.rewind_client.circle(anom['x'], anom['y'], anom['effectiveRadius'], self.rewind_client.rgba_to_int(255, 0, 0 ,20), fill=True)
        for bounty in response[0]['bounties']:
            print(str(bounty))
            self.rewind_client.circle(bounty['x'], bounty['y'], bounty['radius'], self.rewind_client.rgba_to_int(255, 255, 0 ,255), fill=True)

        self.rewind_client.message('draw transports')
        self.rewind_client.end_frame()
        # while True:
        #     time.sleep(1)


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


# def viewer_process(_que: Queue):
#     view = View()
#
#     while True:
#         if _que.empty():
#             continue
#
#         tag, info = _que.get()
#
#         if tag == "Responce":
#             view.update(info)
#
#         if tag == "Bounties":
#             view.bounties_info(info)
#
#         if tag == "DodgeAnomaly":
#             view.anomaly_dodge_info(info)
#
#         if tag == "Kill":
#             view.target_attack(info)


if __name__ == '__main__':
    # que_view = Queue()
    # p = Process(target=viewer_process, args=(que_view,))
    # p.start()

    api = API()
    sol = Solution()
    sol.set_api(api)
    sol.main_process()
