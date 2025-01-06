import requests
import json
import time
import random
from fake_useragent import UserAgent
from colorama import Fore, Style, init

init(autoreset=True)

url = "https://faucet.testnet.mangonetwork.io/gas"

ua = UserAgent()

def get_random_user_agent():
    user_agent = ua.random
    while "Windows" not in user_agent:
        user_agent = ua.random
    return user_agent

# Proxy configuration
PROXY = {
    "http": "http://username:password@ip:port",
    "https": "http://username:password@ip:port"
}

payload = {
    "FixedAmountRequest": {
        "recipient": "0xe177c13ba1ceb4a93eb322a4a96d2dd3a7d739ae1a2847d252caafe39970aa6c"
    }
}

try:
    while True:
        user_agent = get_random_user_agent()

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "chrome-extension://jiiigigdinhhgjflhljdkcelcjfmplnd",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-GPC": "1",
            "User-Agent": user_agent,
            "sec-ch-ua": '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }

        # Adding proxy to the request
        response = requests.post(url, headers=headers, data=json.dumps(payload), proxies=PROXY)
        delay = random.uniform(2, 3)

        if response.status_code == 201:
            data = response.json()
            gas_object = data.get("transferredGasObjects", [{}])[0]
            amount = gas_object.get("amount", "Unknown")
            gas_id = gas_object.get("id", "Unknown")
            tx_digest = gas_object.get("transferTxDigest", "Unknown")

            print(Fore.GREEN + "Success")
            print(Fore.CYAN + f"Amount: {amount}")
            print(Fore.CYAN + f"ID: {gas_id}")
            print(Fore.CYAN + f"Transaction Digest: {tx_digest}")
        else:
            print(Fore.RED + "Failed")
            print(Fore.YELLOW + f"HTTP Status Code: {response.status_code}")
            print(Fore.MAGENTA + f"Response Content: {response.text}")

        print(Fore.BLUE + f"Waiting for {delay:.2f} seconds before next request...\n")
        time.sleep(delay)

except KeyboardInterrupt:
    print(Fore.YELLOW + "Loop stopped by user.")
except Exception as e:
    print(Fore.RED + f"An error occurred: {e}")
