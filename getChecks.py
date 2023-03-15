import requests


class GetChecks:
    def __init__(self, api_url1, api_key1):
        self.api_url1 = api_url1
        self.api_key1 = api_key1
        self.all_checks = []
        self.response = requests.get(self.api_url1, params=api_key1, timeout=5).json()
        for i in range(len(self.response)):
            if self.response[i]["tags"] is not None:
                # print(self.response[i]["name"])
                if "Check type" in self.response[i]["tags"]:
                    check_type = str(self.response[i]["tags"]["Check type"]).split("'")[1]
                else:
                    pass
                    # print(f'{self.response[i]["name"]},  {self.response[i]["id"]},  no check type tag assigned')
                if "Customer" in self.response[i]["tags"]:
                    name = str(self.response[i]["tags"]["Customer"]).split("'")[1]
                elif "Customer1" in self.response[i]["tags"]:
                    name = str(self.response[i]["tags"]["Customer1"]).split("'")[1]
                else:
                    name = str(self.response[i]["name"]).split('-')[0].rstrip()
                    # print(f'{self.response[i]["name"]},  {self.response[i]["id"]},  no customer tag assigned')
                self.check_info = {
                    "id": self.response[i]["id"],
                    "name": name,
                    "value": self.response[i]["value"],
                    "check type": check_type
                }
            else:
                # print(f'{self.response[i]["name"]},  {self.response[i]["id"]},  no tags assigned')
                pass
            self.all_checks.append(self.check_info)
