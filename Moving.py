import math

import numpy as np
import matplotlib.pyplot as plt
import collections
import operator

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
    def best_way_to_bounties(self, transport, bounties):
        t_x = transport['x']
        t_y = transport['y']
        
        # Вверху-слева, вверху-справа, внизу-слева, внизу-справа
        areas = {'UpLeft':0, 'UpRight': 0, 'DownLeft': 0, 'DownRight': 0}
        # Acceptable distance
        acpt_dist = 300
        for bounty in bounties:
            b_x = bounty['x']
            b_y = bounty['y']
            
            # distance_vector
            dist_v = {'x': t_x - b_x, 'y': t_x - b_y}
            if math.hypot(dist_v['x'] < acpt_dist and dist_v['y'] < acpt_dist):
                if dist_v['x'] < 0:
                    if dist_v['y'] < 0:
                        areas['DownLeft'] += bounty['points']
                    else:
                        areas['UpLeft'] += bounty['points']
                    # end if
                else:
                    if dist_v['y'] < 0:
                        areas['DownRight'] += bounty['points']
                    else:
                        areas['UpRight'] += bounty['points']
                    # end if
                # end if
            # end if 
        # end for
        sorted_items = sorted(areas.items(), key=operator.itemgetter(1), reverse=True)
        sorted_areas = dict(sorted_items)
        
        id = transport['id']
        print(f'ID:{id}, close areas:{sorted_areas}')
        return sorted_areas
            
                        
            
            
            
            
            

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
    def anomaly_dodge(_data, _threshold_priority=300) -> dict:
        warning = Moving.anomaly_warning(_data)

        transport_movement_recomendation = {}

        rect = (30, 30)

        vectors = [{"x": x, "y": y} for y in np.arange(-rect[1] // 2, rect[1] // 2, 1)
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

            d = []
            for v in vectors:
                dist = []
                for a_pos in anomaly_pos:
                    dist += [Moving.distance(x + v["x"], a_pos["x"], y + v["y"], a_pos["x"])]

                d += [np.min(dist)]

            vin_vector = vectors[np.argmax(d)]

            vin_vector["x"] += x
            vin_vector["y"] += y

            transport_movement_recomendation[id_transport] = {"vector": vin_vector,
                                                              "priority": "HIGH" if max(
                                                                  d) < _threshold_priority else "LOW"}

            tvx = [x, x + vectors[np.argmin(d)]["x"]]
            tvy = [y, y + vectors[np.argmin(d)]["y"]]

            print(f"dodge anomalies: {transport_movement_recomendation[id_transport]}")
        #     plt.scatter(x, y, color="green")
        #     plt.plot(tvx, tvy, color="green" if transport_movement_recomendation[id_transport]["priority"] == "LOW" else "red")
        # plt.pause(0.1)
        return transport_movement_recomendation

