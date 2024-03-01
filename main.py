import os
import random
import string
import time
import threading
import requests
from discord_webhook import DiscordWebhook

class NitroGen:
    def __init__(self):
        self.fileName = "Nitro Codes.txt"
        self.lock = threading.Lock()
        self.proxy_cycle = None
        self.use_proxyscrape = self.get_user_input("Do you want to use proxyscrape API for proxies? (yes/no): ").lower() == "yes"

        if self.use_proxyscrape:
            self.proxies = self.get_proxies_from_api()
        else:
            self.proxies = self.get_proxies_from_file()

        self.use_webhook = self.get_user_input("Do you want to use a webhook for notifications? (yes/no): ").lower() == "yes"
        self.webhook_url = self.get_webhook_url() if self.use_webhook else None

        self.use_api_key = self.get_user_input("Do you want to include your API key in config.py? (yes/no): ").lower() == "yes"
        if self.use_api_key:
            self.api_key = self.get_api_key_from_user()
            self.save_api_key_to_config()

    def get_proxies_from_api(self):
        api_key = self.get_api_key()
        url = f"https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&apikey={api_key}"
        response = requests.get(url)
        proxies = response.text.split('\r\n')
        return proxies[:100]  # Taking only the first 100 proxies

    def get_proxies_from_file(self):
        proxies_file_path = "proxies.txt"
        if os.path.exists(proxies_file_path):
            with open(proxies_file_path, "r") as file:
                proxies = file.read().splitlines()
            return proxies
        else:
            print("Proxies file not found. Exiting.")
            exit()

    def get_api_key_from_user(self):
        return input("Enter your API key: ")

    def get_api_key(self):
        if self.use_api_key:
            return self.api_key
        else:
            return input("Enter your API key: ")

    def get_webhook_url(self):
        return input("Enter your webhook URL: ")

    def get_user_input(self, question):
        return input(question)

    def save_api_key_to_config(self):
        with open("config.py", "w") as config_file:
            config_file.write(f"api_key = \"{self.api_key}\"")

    def main(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        print(""" GEN V2
                                                        """)
        time.sleep(2)
        self.slowType("Made by: AngerminecraftY", .02)
        print()
        self.slowType(
            "This gen Is NOT An Open source If You Want To Get The Code Contact Me!",
            .02)

        time.sleep(1)
        num = int(input('\nInput How Many Codes to Generate and Check: '))

        print()

        valid = []
        invalid = 0
        webhook_message = ""

        self.proxy_cycle = iter(self.proxies)

        threads = []

        for i in range(0, num, 5):
            thread = threading.Thread(target=self.generate_and_check,
                                      args=(i, min(i + 5, num), valid, invalid))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        webhook_message = f"""
Results:
 Valid: {len(valid)}
 Invalid: {invalid}
 Valid Codes: {', '.join(valid)}
"""

        if self.use_webhook:
            DiscordWebhook(url=self.webhook_url, content=webhook_message).execute()

        print(webhook_message)

        input(
            "\nSuccessfully Generated Nitro Codes! Press Enter 5 times to close the program. Or Refresh The Page to use the gen again"
        )
        [input(i) for i in range(4, 0, -1)]

    def generate_and_check(self, start, end, valid, invalid):
        for i in range(start, end):
            code = "".join(
                random.choices(string.ascii_uppercase + string.digits +
                               string.ascii_lowercase,
                               k=16))
            url = f"https://discord.gift/{code}"

            try:
                proxy = next(self.proxy_cycle)
            except StopIteration:
                self.proxy_cycle = iter(self.proxies)
                proxy = next(self.proxy_cycle)

            result = self.quickChecker(url, proxy)

            if result:
                with self.lock:
                    valid.append(url)
            else:
                with self.lock:
                    invalid += 1

            time.sleep(1)

            if (i + 1) % 10000 == 0:
                with self.lock:
                    self.send_webhook_update(valid, invalid, i + 1)

    def slowType(self, text, speed, newLine=True):
        for i in text:
            print(i, end="", flush=True)
            time.sleep(speed)
        if newLine:
            print()

    def send_webhook_update(self, valid, invalid, codes_generated):
        webhook_message = f"""
Update:
 Codes Generated: {codes_generated}
 Valid: {len(valid)}
 Invalid: {invalid}
"""

        if self.use_webhook:
            DiscordWebhook(url=self.webhook_url, content=webhook_message).execute()

        print(webhook_message)

    def quickChecker(self, nitro, proxy=None):
        url = f"https://discordapp.com/api/v6/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"
        proxies = {'http': proxy} if proxy else None
        response = requests.get(url, proxies=proxies)

        if response.status_code == 200:
            print(f" Valid | {nitro} ")
            return True
        else:
            print(f" Invalid | {nitro} ")
            return False


if __name__ == '__main__':
    Gen = NitroGen()
    Gen.main()
