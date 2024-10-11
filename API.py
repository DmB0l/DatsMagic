import time
import requests
import json
import threading


class API:
    def __init__(self):
        self.token = "66844362b74ce66844362b74d1"
        self.url = "https://games-test.datsteam.dev"
        self.headersPOST = {
            "Content-Type": "application/json",
            "X-Auth-Token": "66844362b74ce66844362b74d1"
        }
        self.headersPUT = {
            "X-Auth-Token": "66844362b74ce66844362b74d1"
        }
        self.headersGET = {
            "Accept": "application/json",
            "X-Auth-Token": "66844362b74ce66844362b74d1"
        }

        # листы
        self.zpots = []
        self.base_centre = None
        self.base_cells = []

        self.enemy_blocks = []
        self.player = []
        self.zombies = []

        # инты
        self.turn = None
        self.turnEndsInMs = None

        self.dataToSend = {}
        self.dataToSend["attack"] = []
        self.dataToSend["build"] = []
        self.dataToSend["moveBase"] = None

        self.name_round = "unknown"

    def __get(self, dopURL):
        fullURL = self.url + dopURL
        print(fullURL)

        response = requests.get(fullURL, headers=self.headersGET)

        if response is not None:
            if response.status_code == 200:
                print("Success", response.status_code)
                return response.json()
            else:
                print("Error:", response.status_code)
                return response.json()
        else:
            with open('empty_json_file.json', 'r') as f:
                return json.load(f)


    def __post(self, dopURL):
        print("data to send:")
        print(self.dataToSend)


        # if self.dataToSend["attack"] == [] and self.dataToSend["build"] == [] and self.dataToSend["moveBase"] is None:
        #     self.write_in_json()
        #     return "Data send is empty"
        # else:
        fullURL = self.url + dopURL
        print(fullURL)

        response = requests.post(fullURL, json=self.dataToSend, headers=self.headersPOST)

        # self.write_in_json()
        self.clear_data_to_send()

        if response is not None:
            if response.status_code == 200:
                print("Success", response.status_code)
                return response.json()
            else:
                print("Error:", response.status_code)
                return response.json()
        else:
            with open('empty_json_file.json', 'r') as f:
                return json.load(f)


    def __put(self, dopURL):
        fullURL = self.url + dopURL
        print(fullURL)

        response = requests.put(fullURL, headers=self.headersPUT)
        print("response: ")
        print(response)

        if response is not None:
            if response.status_code == 200:
                print("Success", response.status_code)
                return response.json()
            else:
                print("Error:", response.status_code)
                return response.json()
        else:
            with open('empty_json_file.json', 'r') as f:
                return json.load(f)

    def sendReqCommand(self):
        return self.__post("/play/zombidef/command")

    def sendReqParticipate(self):
        return self.__put("/play/zombidef/participate")

    def sendReqUnits(self):
        return self.__get("/play/zombidef/units")

    def sendReqWorld(self):
        return self.__get("/play/zombidef/world")

    def sendReqRounds(self):
        return self.__get("/rounds/zombidef")

    def start(self):
        requestThread = threading.Thread(target=self.__starting)
        requestThread.start()

    def __starting(self):
        while (True):
            response = self.sendReqRounds()
            now_round = "unknown"

            for i in range(len(response["rounds"])):
                # print(response["rounds"][i])
                if response["rounds"][i]["status"] == "active":
                    now_round = response["rounds"][i]["name"]

            if self.name_round != now_round:
                response = self.sendReqParticipate()
                print(response)
                if "startsInSec" in response:
                    self.name_round = now_round
                    while response["startsInSec"] > 2:
                        time.sleep(1)
                        response = self.sendReqParticipate()
                        print(response)
                        if "startsInSec" not in response:
                            break
                elif "errCode" in response and response["errCode"] == 1001:
                    self.name_round = now_round
                else:
                    time.sleep(1)

            elif now_round == "unknown":
                self.zpots = []
                self.base_cells = []
                self.base_centre = None
                self.enemy_blocks = []
                self.player = []
                self.zombies = []
                self.turn = None
                self.turnEndsInMs = None

                time.sleep(1)
            else:
                data_world = self.sendReqWorld()

                # with open('LOG_World_' + now_round + '.json', 'a') as f:
                #     if f.tell() == 0:  # check if the file is empty
                #         f.write('[')  # start the JSON array
                #     else:
                #         f.write(',\n')  # add a comma and newline to separate entries
                #     json.dump(data_world, f, indent=4)

                if "zpots" in data_world and data_world["zpots"] is not None and data_world["zpots"] != "null":
                    self.zpots = data_world['zpots']
                else:
                    self.zpots = []



                data_units = self.sendReqUnits()

                # with open('LOG_Units_' + now_round + '.json', 'a') as f:
                #     if f.tell() == 0:  # check if the file is empty
                #         f.write('[')  # start the JSON array
                #     else:
                #         f.write(',\n')  # add a comma and newline to separate entries
                #     json.dump(data_units, f, indent=4)

                if "base" in data_units and data_units["base"] is not None and data_units["base"] != "null":
                    base = data_units["base"]
                    self.base_cells = []
                    for j in range(len(base)):
                        if "isHead" in base[j]:
                            self.base_centre = base[j]
                        else:
                            self.base_cells.append(base[j])
                else:
                    self.base_cells = []
                    self.base_centre = None

                if "enemyBlocks" in data_units and "enemyBlocks" in data_units and data_units["enemyBlocks"] is not None and data_units["enemyBlocks"] != "null":
                    self.enemy_blocks = data_units['enemyBlocks']
                else:
                    self.enemy_blocks = []

                if "player" in data_units and data_units["player"] is not None and data_units["player"] != "null":
                    self.player = data_units['player']
                else:
                    self.player = []

                if "zombies" in data_units and data_units["zombies"] is not None and data_units["zombies"] != "null":
                    self.zombies = data_units['zombies']
                else:
                    self.zombies = []

                if "turn" in data_units and data_units["turn"] is not None and data_units["turn"] != "null":
                    self.turn = data_units['turn']
                else:
                    self.turn = None

                if "turnEndsInMs" in data_units and data_units["turnEndsInMs"] is not None and data_units["turnEndsInMs"] != "null":
                    self.turnEndsInMs = data_units['turnEndsInMs']
                else:
                    self.turnEndsInMs = None

                if self.turnEndsInMs:
                    time.sleep(self.turnEndsInMs/1000 + 0.05)
                else:
                    time.sleep(0.5)

    def read_log(self):
        logThread = threading.Thread(target=self.__reading_log)
        logThread.start()

    def __reading_log(self):
        with open('LOG_World_test-day1-9.json', 'r') as f:
            data_world = json.load(f)
        with open('LOG_Units_test-day1-9.json', 'r') as f:
            data_units = json.load(f)

        for i in range(len(data_units)):
            if i < len(data_world):
                if data_world[i]["zpots"] is not None and data_world[i]["zpots"] != "null":
                    self.zpots.append(data_world[i]['zpots'])
                else:
                    self.zpots = []

                if data_units[i]["base"] is not None and data_units[i]["base"] != "null":
                    base = data_units[i]["base"]
                    self.base_cells = []

                    for j in range(len(base)):
                        if "isHead" in base[j]:
                            self.base_centre = base[j]
                        else:
                            self.base_cells.append(base[j])
                else:
                    self.base_cells = []
                    self.base_centre = None

                if data_units[i]["enemyBlocks"] is not None and data_units[i]["enemyBlocks"] != "null":
                    self.enemy_blocks = data_units[i]["enemyBlocks"]
                else:
                    self.enemy_blocks = []

                if data_units[i]["player"] is not None and data_units[i]["player"] != "null":
                    self.player = data_units[i]["player"]
                else:
                    self.player = []

                if data_units[i]["zombies"] is not None and data_units[i]["zombies"] != "null":
                    self.zombies = data_units[i]["zombies"]
                else:
                    self.zombies = []

                if data_units[i]["turn"] is not None and data_units[i]["turn"] != "null":
                    self.turn = data_units[i]["turn"]
                else:
                    self.turn = None

                if data_units[i]["turnEndsInMs"] is not None and data_units[i]["turnEndsInMs"] != "null":
                    self.turnEndsInMs = data_units[i]["turnEndsInMs"]
                else:
                    self.turnEndsInMs = None

                if self.turnEndsInMs:
                    time.sleep(0.5)

    def write_attack(self, blockId, target):
        dataToAttack = {"blockId": blockId, "target": target}
        self.dataToSend["attack"].append(dataToAttack)

    def write_build(self, x, y):
        dataToBuild = {"x": x, "y": y}
        self.dataToSend["build"].append(dataToBuild)

    def write_move_base(self, x, y):
        dataToMoveBase = {"x": x, "y": y}
        self.dataToSend["moveBase"] = dataToMoveBase

    def clear_data_to_send(self):
        self.dataToSend = {}
        self.dataToSend["attack"] = []
        self.dataToSend["build"] = []
        self.dataToSend["moveBase"] = None


    def write_in_json(self):
        with open('LOG_Req_' + self.name_round + '.json', 'a') as f:
            if f.tell() == 0:  # check if the file is empty
                f.write('[')  # start the JSON array
            else:
                f.write(',\n')  # add a comma and newline to separate entries
            json.dump(self.dataToSend, f, indent=4)
            f.write(']')  # start the JSON array


if __name__ == '__main__':
    print("run the solution!")
    # api = API()
    # api.start()

    # data = {'error': 2682}
    # with open('empty_json_file.json', 'w') as f:
    #     json.dump(data, f)


    # api.read_log()
    #
    # api.write_attack("f47ac10b-58cc-0372-8562-0e02b2c3d479", {"x": 1, "y": 1})
    # api.write_build(1, 1)
    # api.write_build(2, 11)
    # api.write_move_base(1, 2)
    #
    # api.write_in_json()



    # print(api.base)


    # response = api.sendReqRounds()

    # print(len(response["rounds"]))
    # for i in range(len(response["rounds"])):
    #     print(response["rounds"][i])
    #     if response["rounds"][i]["status"] == "active":
    #         now_round = response["rounds"][i]["name"]
    #
    # print(now_round)

    # response = api.sendReqParticipate()
    # print(response)

    # requestThread = threading.Thread(target=get_world_units)
    # requestThread.start()

    # requestThread = threading.Thread(target=read_log)
    # requestThread.start()

    # while(True):
    #     response = api.sendReqWorld()
    #     print(response)
    #     with open('LOG_World_' + now_round + '.json', 'a') as f:
    #         if f.tell() == 0:  # check if the file is empty
    #             f.write('[')  # start the JSON array
    #         else:
    #             f.write(',\n')  # add a comma and newline to separate entries
    #         json.dump(response, f, indent=4)
    #
    #     response = api.sendReqUnits()
    #     print(response)
    #
    #     with open('LOG_Units_' + now_round + '.json', 'a') as f:
    #         if f.tell() == 0:  # check if the file is empty
    #             f.write('[')  # start the JSON array
    #         else:
    #             f.write(',\n')  # add a comma and newline to separate entries
    #         json.dump(response, f, indent=4)
    #
    #     time.sleep(0.5)



