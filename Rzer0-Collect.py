import os
import requests
from bs4 import BeautifulSoup

def download_file(url, folder, html_filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Extract the filename from the URL, handling cases where it ends with '/'
        filename = url.split('/')[-1]
        if not filename:  # If the URL ends with '/', use the HTML filename with '_download.html'
            filename = os.path.splitext(html_filename)[0] + '_download.html'
        
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filepath}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def main():
    base_dir = 'RingZer0'
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    soup = BeautifulSoup(f, 'html.parser')
                    download_divs = soup.find_all('div', class_='download')
                    for div in download_divs:
                        a_tag = div.find('a')
                        if a_tag and 'href' in a_tag.attrs:
                            href = a_tag['href']
                            if href.startswith('http'):
                                download_file(href, root, file)

if __name__ == "__main__":
    main()