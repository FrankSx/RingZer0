import requests
from bs4 import BeautifulSoup
import re
import os

login_url = 'https://ringzer0ctf.com/login'
username = 'Your_UserName'
password = 'Your_Password'
session = requests.Session()
response = session.get(login_url)

if response.status_code == 200:
    csrf_token_match = re.search(r"var\s+\w+\s*=\s*'([a-f0-9]{32})';", response.text)
    if csrf_token_match:
        csrf_token = csrf_token_match.group(1)
        payload = {
            'username': username,
            'password': password,
            'csrf': csrf_token,
            'check': 'true'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': login_url,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://ringzer0ctf.com',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Priority': 'u=0, i'
        }
        login_response = session.post(login_url, headers=headers, data=payload)
        if login_response.status_code == 200:
            os.makedirs(base_dir, exist_ok=True)
            with open('challenges.txt', 'r') as file:
                challenge_entries = file.readlines()
            for entry in challenge_entries:
                entry = entry.strip()
                if not entry:
                    continue
                if entry.startswith("Category:"):
                    current_category = entry.split("Category:")[1].strip()
                    category_folder = current_category.replace(" ", "_")
                    os.makedirs(category_folder, exist_ok=True)
                else:
                    challenge_name, challenge_url = entry.split(': ', 1)
                    challenge_folder = os.path.join(category_folder, challenge_name.replace(" ", "_"))
                    os.makedirs(challenge_folder, exist_ok=True)
                    challenge_response = session.get(challenge_url)
                    if challenge_response.status_code == 200:
                        challenge_file_name = f"{challenge_name.replace(' ', '_')}.html"
                        with open(os.path.join(challenge_folder, challenge_file_name), 'w', encoding='utf-8') as f:
                            f.write(challenge_response.text)
                    else:
                        print(f"Failed to fetch {challenge_url}. Status code: {challenge_response.status_code}")
        else:
            print("Login failed. Please check your credentials.")
            print("Response content:", login_response.text)
else:
    print(f"Failed to retrieve the login page. Status code: {response.status_code}")