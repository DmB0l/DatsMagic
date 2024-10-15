import copy
import math

import numpy as np


class Moving:
    def __init__(self):
        self.asd = 0

    def move(self, x, y, transport, max_speed):
        transport_x = transport['x']
        transport_y = transport['y']

        transport_velocity_x = transport['velocity']['x']
        transport_velocity_y = transport['velocity']['y']

        move_vector = {'x': x - transport_x, 'y': y - transport_y}
        length_move_vector = math.hypot(move_vector['x'], move_vector['y'])

        koef = max_speed / length_move_vector

        move_vector['x'] *= koef
        move_vector['y'] *= koef

        return move_vector

    def stop(self, transport):
        transport_velocity_x = transport['velocity']['x']
        transport_velocity_y = transport['velocity']['y']

        move_vector = {'x': transport_velocity_x * -1, 'y': transport_velocity_y * -1}

        return move_vector
    
    # Поиск наибольшего скопления монет (мб суммировать их?)
    # Дорога к центру (?)
    @staticmethod
    def bounties_way(tr, _data, _threshold_priority=300) -> dict:
        # transports = _data['transports']
        bounties = _data['bounties']
        norm_distance = 400

        # for tr in transports:
        # Позиция в текущий тик
        tr_x = tr['x']
        tr_y = tr['y']
        # Вектор скорости
        tr_vx = tr['velocity']['x']
        tr_vy = tr['velocity']['y']
        # Позиция в следующий тик
        tr_xvx = tr_x + tr_vx
        tr_yvy = tr_y + tr_vy

        best_bnt = bounties[0]
        min_distance = 99999

        best_bounty = {'x': tr_xvx, 'y': tr_yvy}
        for bnt in bounties:
            bnt_x = bnt['x']
            bnt_y = bnt['y']
            tr_bnt_distance = Moving.distance(tr_x, bnt_x, tr_y, bnt_y)
            print(f"tr_bnt_distance={tr_bnt_distance} tr_x={tr_x} tr_y={tr_y} bnt_x={bnt_x} bnt_y={bnt_y}")
            
            if (tr_bnt_distance < norm_distance):
                tr_v_bnt_distance = Moving.distance(tr_xvx, bnt_x, tr_yvy, bnt_y)
                if (tr_v_bnt_distance - tr_bnt_distance < min_distance):
                    min_distance = tr_v_bnt_distance - tr_bnt_distance
                    best_bnt = bnt
                    print(f"Update. Min dist={min_distance}, size={len(bounties)}")

        best_bounty['x'] = best_bnt['x']
        best_bounty['y'] = best_bnt['y']
        return best_bounty
        
            
                        
            
            
            
            
            

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
    def anomaly_dodge(_data, _threshold_priority=1000) -> dict:
        warning = Moving.anomaly_warning(_data)

        transport_movement_recomendation = {}

        rect = (6, 6)
        m = 10
        vectors = [{"x": x*m, "y": y*m} for y in np.arange(-rect[1] // 2, rect[1] // 2, 1)
                   for x in np.arange(-rect[0] // 2, rect[0] // 2, 1)]

        # plt.cla()
        for id_transport in warning.keys():
            anomaly_pos = []

            for a in warning[id_transport]:
                anom = a["anom"]
                anomaly_pos += [{"x": anom["x"], "y": anom["y"]}]

                avx, avy = [anom["x"], anom["x"] + anom["velocity"]["x"]], [anom["y"],
                                                                            anom["y"] + anom["velocity"]["y"]]
                # plt.scatter(anom["x"], anom["y"], color="magenta")
                # plt.plot(avx, avy)

            if not len(anomaly_pos):
                transport_movement_recomendation[id_transport] = {"vector": None,
                                                                  "priority": "LOW"}
                continue

            transport = warning[id_transport][0]["transport"]
            x = transport["x"]
            y = transport["y"]
            # plt.scatter(x, y, color="green")

            d = []
            for v in vectors:
                tvx = [x, x + v["x"]]
                tvy = [y, y + v["y"]]
                # plt.plot(tvx, tvy, color="red")

                dist = []
                for a_pos in anomaly_pos:
                    dist += [Moving.distance(x + v["x"], a_pos["x"], y + v["y"], a_pos["y"])]

                d += [np.min(dist)]
                ...

            vin_vector = copy.copy(vectors[np.argmax(d)])

            vin_vector["x"] += x
            vin_vector["y"] += y

            transport_movement_recomendation[id_transport] = {"vector": vin_vector,
                                                              "priority": "HIGH" if min(
                                                                  d) < _threshold_priority else "LOW"}

        return transport_movement_recomendation

