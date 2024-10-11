import time
import requests
import json
import threading


class API:
    def __init__(self):
        self.token = "67066aec845f267066aec845f7"
        self.url = "https://games-test.datsteam.dev"
        self.headersPOST = {
            "Content-Type": "application/json",
            "X-Auth-Token": "67066aec845f267066aec845f7"
        }
        self.headersPUT = {
            "X-Auth-Token": "67066aec845f267066aec845f7"
        }
        self.headersGET = {
            "Accept": "application/json",
            "X-Auth-Token": "67066aec845f267066aec845f7"
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

        self.dataToSend = {"transport": []}

        self.name_round = "unknown"
        self.round_repeat = -1

    def __get(self, dopURL):
        fullURL = self.url + dopURL
        print(fullURL)

        response = requests.get(fullURL, headers=self.headersGET)

        if response is not None:
            return response.status_code, response.json()
        else:
            return None, None

    def __post(self, dopURL):
        print("data to send:")
        print(self.dataToSend)

        fullURL = self.url + dopURL
        print(fullURL)

        response = requests.post(fullURL, json=self.dataToSend, headers=self.headersPOST)

        self.dataToSend = {"transport": []}

        if response is not None:
            return response.status_code, response.json()
        else:
            return None, None

    def __put(self, dopURL):
        fullURL = self.url + dopURL
        print(fullURL)

        response = requests.put(fullURL, headers=self.headersPUT)

        if response is not None:
            return response.status_code, response.json()
        else:
            return None, None

    def sendReqCommand(self):
        return self.__post("/play/magcarp/player/move")

    def sendReqRounds(self):
        return self.__get("/rounds/magcarp")

    def start(self):
        while (True):
            status_code, response = self.sendReqRounds()

            print('ROUNDS')
            print('status_code: ' + str(status_code))
            print('response: ' + str(response))

            #### ЗАПРОС НА РАУНДЫ (ИЩЕТСЯ И ВЫБИРАЕТСЯ АКТИВНЫЙ) ####

            if status_code is not None and response is not None and status_code == 200:
                with open('LOG_Rounds.json', 'a') as f:
                    if f.tell() == 0:  # check if the file is empty
                        f.write('[')  # start the JSON array
                    else:
                        f.write(',\n')  # add a comma and newline to separate entries
                    json.dump(response, f, indent=4)

                now_round = "unknown"

                for i in range(len(response["rounds"])):
                    # print(response["rounds"][i])
                    if response["rounds"][i]["status"] == "active":
                        now_round = response["rounds"][i]["name"]
                        break

                if now_round != "unknown":
                    self.name_round = now_round
                    self.dataToSend = {"transport": []}
                    status_code, response = self.sendReqCommand()
                    print('GAME')
                    print('status_code: ' + str(status_code))
                    print('response: ' + str(response))
                    json_string = json.dumps(response, indent=4)
                    # Print the JSON string to the console
                    print(json_string)

                    with open('LOG_Game_' + now_round + '.json', 'a') as f:
                        if f.tell() == 0:  # check if the file is empty
                            f.write('[')  # start the JSON array
                        else:
                            f.write(',\n')  # add a comma and newline to separate entries
                        json.dump(response, f, indent=4)

                    if status_code is not None and response is not None and status_code == 200:
                        return response
                    else:
                        time.sleep(0.4)
                else:
                    time.sleep(0.4)
            else:
                time.sleep(0.4)

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

    def write_data_to_build(self, transport):
        self.dataToSend = transport

    def write_in_json(self):
        with open('LOG_Req_' + self.name_round + '.json', 'a') as f:
            if f.tell() == 0:  # check if the file is empty
                f.write('[')  # start the JSON array
            else:
                f.write(',\n')  # add a comma and newline to separate entries
            json.dump(self.dataToSend, f, indent=4)
            f.write(']')  # start the JSON array


if __name__ == '__main__':
    print("run other main!")
    api = API()
    api.start()
