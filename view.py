import matplotlib.pyplot as plt
import numpy as np


class View:
    def __init__(self):
        plt.ion()
        self.m_fig, self.m_axs = plt.subplots(1, 1, figsize=(5, 5))

    def update(self, _info):
        wanted = _info["wantedList"]
        map_size = _info["mapSize"]
        enemies = _info["enemies"]
        anomalies = _info["anomalies"]
        bounties = _info["bounties"]

        # me = _info[""]

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

        plt.pause(0.1)
        ...


if __name__ == '__main__':
    import json

    with open('LOG_Game_test-day1-1.json', 'r') as file:
        test_data = json.load(file)

    v = View()
    v.update(test_data)
    v.update()
