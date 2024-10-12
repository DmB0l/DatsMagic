import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.use('TkAgg')


class View:
    def __init__(self):
        plt.ion()
        self.m_fig, self.m_axs = plt.subplots(1, 1, figsize=(10, 10))
        self.m_axs.set_facecolor("black")

        self.m_track = {}
        self.m_track_store = 10
        plt.ion()

    def anomaly_dodge_info(self, _info):
        transports, info = _info

        for transport in transports:
            if info[transport["id"]]["vector"]:
                self.m_axs.plot([transport["x"], info[transport["id"]]["vector"]["x"] + 300], [transport["y"],
                                                                                              info[transport["id"]][
                                                                                                  "vector"]["y"] + 300],
                                color="#33CCCC")
        plt.pause(0.05)
        ...

    def bounties_info(self, _info):
        transport, bounty_pos = _info
        self.m_axs.plot([transport["x"], bounty_pos["x"]], [transport["y"], bounty_pos["y"]], color="yellow")
        # print()
        plt.pause(0.05)
        ...

    def target_attack(self, _targets):
        for t in _targets:
            if t["x"] != 0 and t["y"] != 0:
                self.m_axs.scatter(t["x"], t["y"], s=250, alpha=0.4, color="#FF0000")

        ...

    def update(self, _info):
        self.m_axs.cla()

        wanted = _info["wantedList"]
        map_size = _info["mapSize"]
        enemies = _info["enemies"]
        anomalies = _info["anomalies"]
        bounties = _info["bounties"]

        transports = _info["transports"]

        if not len(self.m_track.keys()):
            for transport in transports:
                self.m_track[transport["id"]] = {"x": [transport["x"]], "y": [transport["y"]]}

        self.m_axs.set_ylim(0, map_size["y"])
        self.m_axs.set_xlim(0, map_size["x"])

        for en in enemies:
            evx, evy = [en["x"], en["x"] + en["velocity"]["x"]], [en["y"], en["y"] + en["velocity"]["y"]]
            self.m_axs.scatter(en["x"], en["y"], c="red")
            if en['shieldLeftMs'] > 4000:
                self.m_axs.scatter(en["x"], en["y"], c="red", alpha=0.1, s=55)

            self.m_axs.plot(evx, evy, color="red")

        for want in wanted:
            wvx, wvy = [want["x"], want["x"] + want["velocity"]["x"]], [want["y"], want["y"] + want["velocity"]["y"]]
            self.m_axs.scatter(want["x"], want["y"], c="blue")
            self.m_axs.plot(wvx, wvy, color="magenta")

        for anom in anomalies:
            avx, avy = [anom["x"], anom["x"] + anom["velocity"]["x"]], [anom["y"], anom["y"] + anom["velocity"]["y"]]
            self.m_axs.scatter(anom["x"], anom["y"], s=anom["radius"], c="magenta")
            self.m_axs.scatter(anom["x"], anom["y"], alpha=0.1, s=anom["effectiveRadius"], c="magenta")
            self.m_axs.plot(avx, avy, color="magenta")

        for bounty in bounties:
            self.m_axs.scatter(bounty["x"], bounty["y"], s=bounty["radius"], c="yellow")

        for transport in transports:
            tvx, tvy = [transport["x"], transport["x"] + transport["velocity"]["x"] + 100], [transport["y"],
                                                                                             transport["y"] +
                                                                                             transport["velocity"][
                                                                                                 "y"] + 100]
            self.m_axs.scatter(transport["x"], transport["y"], alpha=transport["health"] / 100, c="green")
            self.m_track[transport["id"]]["x"].append(transport["x"])
            self.m_track[transport["id"]]["y"].append(transport["y"])

            self.m_axs.plot(tvx, tvy, color="green")
            self.m_axs.plot(self.m_track[transport["id"]]["x"], self.m_track[transport["id"]]["y"], color="green",
                            linestyle='-')

            if len(self.m_track[transport["id"]]["x"]) > self.m_track_store:
                self.m_track[transport["id"]]["x"] = self.m_track[transport["id"]]["x"][1:]
                self.m_track[transport["id"]]["y"] = self.m_track[transport["id"]]["y"][1:]

        plt.pause(0.05)


if __name__ == '__main__':
    import json

    with open('LOG_Game_test-day1-1.json', 'r') as file:
        test_data = json.load(file)

    v = View()
    v.update(test_data)
    v.update(test_data)
    plt.show()
