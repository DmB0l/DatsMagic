import math

import numpy as np
import matplotlib.pyplot as plt
import collections

class Moving:
    def __init__(self):
        self.asd = 0

    def move(self, x, y, transport, max_speed):
        transport_x = transport['x']
        transport_y = transport['y']

        transport_velocity_x = transport['velocity']['x']
        transport_velocity_y = transport['velocity']['y']

        move_vector = {'x': x - transport_x, 'y': y - transport_y}
        length_move_vector = math.hypot(move_vector['x'], move_vector['x'])

        koef = max_speed / length_move_vector

        move_vector['x'] *= koef
        move_vector['y'] *= koef

        return move_vector

    def stop(self, transport):
        transport_velocity_x = transport['velocity']['x']
        transport_velocity_y = transport['velocity']['y']

        move_vector = {'x': transport_velocity_x * -1, 'y': transport_velocity_y * -1}

        return move_vector

    @staticmethod
    def distance(x1, x2, y1, y2):
        return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    @staticmethod
    def angle(x1, x2, y1, y2):
        dx = x1 - x2
        dy = y1 - y2
        return np.atan2(dy, dx) * 180/np.pi + 180

    @staticmethod
    def interpolate(x1, x2, y1, y2, x):
        return y1 + (x - x1) * (y2 - y1) / (x2 - x1)

    @staticmethod
    def anomaly_warning(_data):
        """
        Поиск аномалий в которые мы попали

        :param _data:
        :return: список вхождений
        """
        transports = _data["transports"]
        anomalies = _data["anomalies"]

        tr_warning = {}

        for anom in anomalies:
            x, y = anom["x"], anom["y"]
            for tr in transports:
                x1, y1 = tr["x"], tr["y"]
                dist = Moving.distance(x, x1, y, y1)

                if tr["id"] not in tr_warning.keys():
                    tr_warning[tr["id"]] = []

                if dist < anom["effectiveRadius"]:
                    tr_warning[tr["id"]].append({"distance": dist, "anom": anom, "transport": tr})

                "Опасная аномалия убивающая при вхождении в зону"
                if anom["radius"] == anom["effectiveRadius"] and dist < anom["radius"] + 200:
                    tr_warning[tr["id"]].append({"distance": dist, "anom": anom, "transport": tr})

        return tr_warning

    @staticmethod
    def anomaly_dodge(_data):
        warning = Moving.anomaly_warning(_data)

        transport_movement_recomendation = {}

        movement = ["lefttop", "leftbottom", "righttop", "rightbottom"]

        for id_transport in warning.keys():
            side = []
            for w in warning[id_transport]:
                anom = w["anom"]
                transport = w["transport"]

                tx, ty = transport["x"], transport["y"]
                ax, ay = anom["x"], anom["y"]

                pos = ""
                if ax < tx:
                    pos += "left"
                elif ax > tx:
                    pos += "right"

                if ay < ty:
                    pos += "bottom"
                elif ay > ty:
                    pos += "top"

                side.append(pos)

            for m in movement:
                if m not in side:
                    transport_movement_recomendation[id_transport] = m

        return transport_movement_recomendation
            # dict(collections.Counter(positions))
