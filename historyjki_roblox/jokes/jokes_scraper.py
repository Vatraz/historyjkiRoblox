import requests
import time

from bs4 import BeautifulSoup

from historyjki_roblox.resource_manager import ResourceManager


class KawalyTjaPlScraper:

    def __init__(self, category: str):
        self.category = category
        self.order = "od_najlepszych"
        self.resource_manager = ResourceManager()

    def download_all_pages(self):
        existing_jokes = self.resource_manager.get_jokes()

        base_url = f"https://kawaly.tja.pl/{self.category}"
        page, saved = 1, 0

        while True:
            url = base_url
            params = {"st": page}

            response = requests.post(
                base_url, params=params, data={"poukladaj_wedlug": self.order}
            )
            time.sleep(2)

            if response.status_code != 200:
                print("Coś nie tak...")
                break

            soup = BeautifulSoup(response.content, "html.parser")
            jokes = elements_with_class_dd = soup.find_all(class_="tresc")

            if len(jokes) == 0:
                print("Żarty się skończyły...")
                break

            for joke in jokes:
                joke_a = joke.find(class_="lista_czcionka")
                if joke_a:
                    lines = tuple([line.strip() for line in joke_a.stripped_strings])
                    if lines in existing_jokes:
                        continue
                    existing_jokes.add(lines)
                    self.resource_manager.save_joke(lines, self.category)
                    saved += 1

            print(
                f"{url}, strona: {page}, status: {response.status_code}, liczba żartów na stronie: {len(jokes)}, zapisano: {saved}"
            )
            page += 1


if __name__ == "__main__":
    scraper = KawalyTjaPlScraper("o-blondynkach")
    scraper.download_all_pages()
