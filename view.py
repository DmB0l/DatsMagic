import matplotlib.pyplot as plt
import numpy as np


class View:
    def __init__(self):
        plt.ion()
        self.m_fig, self.m_axs = plt.subplots(1, 1, figsize=(5, 5))
        self.m_axs.set_facecolor("black")

        self.m_track = {}
        self.m_track_store = 10

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
            self.m_axs.scatter(en["x"], en["y"], c="red")

        for want in wanted:
            self.m_axs.scatter(want["x"], want["y"], c="blue")

        for anom in anomalies:
            self.m_axs.scatter(anom["x"], anom["y"], s=anom["radius"], c="magenta")

        for bounty in bounties:
            self.m_axs.scatter(bounty["x"], bounty["y"], s=bounty["radius"], c="yellow")

        for transport in transports:
            self.m_axs.scatter(transport["x"], transport["y"], alpha=transport["health"] / 100, c="green")
            self.m_track[transport["id"]]["x"].append(transport["x"])
            self.m_track[transport["id"]]["y"].append(transport["y"])

            self.m_axs.plot(self.m_track[transport["id"]]["x"], self.m_track[transport["id"]]["y"], color="green",
                            linestyle='-')

            if len(self.m_track[transport["id"]]["x"]) > self.m_track_store:
                self.m_track[transport["id"]]["x"] = self.m_track[transport["id"]]["x"][1:]
                self.m_track[transport["id"]]["y"] = self.m_track[transport["id"]]["y"][1:]

        plt.pause(0.1)


if __name__ == '__main__':
    import json

    with open('LOG_Game_test-day1-1.json', 'r') as file:
        test_data = json.load(file)

    v = View()
    v.update(test_data)
    v.update(test_data)
    plt.show()
