import requests
import json
import time


class Dreamy:
    def get(self, URL=None, headers=None, cooldown=15):
        if not URL:
            raise Exception("No URL supplied")

        successful = False
        while not successful:
            try:
                response = requests.get(
                    URL,
                    headers=headers
                ).json()
                cooldown = response["cooldown"]
                successful = True
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(response)

        time.sleep(cooldown)
        # print(cooldown)
        return response

    def post(self, URL=None, headers=None, data={}, cooldown=15):
        if not URL:
            return {"errors": ["No URL supplied"]}

        successful = False
        while not successful:
            try:
                response = requests.post(
                    URL,
                    headers=headers,
                    data=json.dumps(data),
                ).json()
                cooldown = response["cooldown"]
                successful = True
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(response)

        time.sleep(cooldown)
        # print(cooldown)
        return response


dreamy = Dreamy()
