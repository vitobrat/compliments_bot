import requests
import re
from bs4 import BeautifulSoup

# URL страницы с комплиментами
URLs = ["https://datki.net/komplimenti/lubimoy/"]


def fetch_compliments(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Replace all <br> tags with newline characters
        for br in soup.find_all('br'):
            br.replace_with('\n')

        # Предполагается, что комплименты находятся в тегах <p> или <div>
        compliments = []
        for element in soup.find_all('p'):  # Замените на соответствующие теги
            text = element.get_text()
            text += "\n$$"
            if not bool(re.match(r"Автор:.*", text)):
                compliments.append(text)
        return compliments
    else:
        print(f"Failed to retrieve page, status code: {response.status_code}")
        return []


def save_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for compliment in data:
            file.write(f"{compliment}\n")


def main():
    compliments = []
    for url in URLs:
        compliments.extend(fetch_compliments(url)[1:-2])
    print(compliments)
    if compliments:
        save_to_file(compliments, 'compliments.txt')
        print(f"Saved {len(compliments)} compliments to 'compliments.txt'")
    else:
        print("No compliments found or failed to fetch the page.")


if __name__ == '__main__':
    main()
