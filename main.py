# main.py
import os
import random
import string
import time
import threading
import requests
from discord_webhook import DiscordWebhook
from config import api_key, webhook_url

class NitroGen:
    def __init__(self):
        self.fileName = "Nitro Codes.txt"
        self.proxies = self.get_proxies()
        self.lock = threading.Lock()
        self.proxy_cycle = self.get_proxy_cycle()

    def get_proxies(self):
        url = f"https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&apikey={api_key}"
        response = requests.get(url)
        proxies = response.text.split('\r\n')
        return proxies[:100]

    def get_proxy_cycle(self):
        while True:
            for proxy in self.proxies:
                yield proxy

    def main(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        print(""" GEN V1, Made with love for all discord users without Discord Nitro
                                                        """)
        time.sleep(2)
        self.slowType("Enjoy this!", .02)
        print()
        self.slowType(
            "This generator is solely made for educational purposes, I am not responsible for what you do with it, good luck with your codes!",
            .02)

        time.sleep(1)
        num = int(input('\nInput How Many Codes to Generate and Check: '))

        print()

        valid = []
        invalid = 0
        webhook_message = ""

        threads = []

        for i in range(0, num, 5):  # Incrementamos de 5 en 5
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

        DiscordWebhook(url="https://discord.com/api/webhooks/your_webhook_url_here", content=webhook_message).execute()

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
                self.proxy_cycle = self.get_proxy_cycle()
                proxy = next(self.proxy_cycle)

            result = self.quickChecker(url, proxy)

            if result:
                with self.lock:
                    valid.append(url)
            else:
                with self.lock:
                    invalid += 1

            time.sleep(1)

            if (
                    i + 1
            ) % 10000 == 0:  # Cambia el número para ajustar la frecuencia de actualización
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

        DiscordWebhook(url=webhook_url, content=webhook_message).execute()

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
