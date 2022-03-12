import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import sys, argparse

class MALScraper:
    def __init__(self, proxies = None):
        self.titles = []
        self.mal_genres = ["Action", "Adventure", "Boys Love", "Comedy", "Drama", "Fantasy", "Girls Love", "Horror", "Mystery", "Romance", "Sci-Fi", "Slice of Life",
              "Sports", "Supernatural", "Ecchi", "Hentai", "Cars", "Demons", "Game", "Harem", "Historical", "Martial Arts", "Mecha", "Military", "Music",
              "Parody", "Police", "Psychological", "Samurai", "School", "Space", "Supew Power", "Vampire"]
        self.proxies = proxies
        self.proxy_counter = 0

    def get_id_from_link(self, url):
        return int(url.split('/')[4])

    def get_mal_anime_link(self, id):
        return f"https://myanimelist.net/anime/{id}"

    def scrape_anime(self, start = 0, lim = 1000):
        counter = start
        while counter < lim:
            url = f"https://myanimelist.net/topanime.php?limit={counter}"
            req = requests.get(url)
            if req.status_code != 200:
                print(f"Error scraping top anime page for limit {counter}, status code {req.status_code}")
            else:
                soup = BeautifulSoup(req.content, "html.parser")
                tds = soup.select("td.title.al.va-t.word-break")
                for td in tds:
                    self.titles.append(self.get_title(td.find('a')['href']))
                    counter = counter + 1
                    if counter % 100 == 0:
                        print(f'{counter-start} titles scraped')
                        time.sleep(180) # use if scraping without proxy to avoid IP ban
                    if counter >= lim:
                        break
    
    def get_title(self, url):
        id = self.get_id_from_link(url)
        if self.proxies == None:
            req = requests.get(url)
        else:
            print(self.proxy_counter)
            req = requests.get(url, proxies = self.proxies[self.proxy_counter])
            self.proxy_counter = (self.proxy_counter + 1) % self.proxies.size()
        title_dict = {"id": id, "Title": None, "Score": None, "Scored by": None, "Members": None,
                 "Genres": None, "Status": None}
        if req.status_code != 200:
            print(f"Error scraping the page with id {id}, status code {req.status_code}")
        else:
            soup = BeautifulSoup(req.content, "html.parser")
            title_dict["Title"] = soup.find(class_="title-name").text
            title_dict["Score"] = float(soup.find("span", class_="score-label").text)
            title_dict["Scored by"] = int(soup.find("span", itemprop="ratingCount").text)
            title_dict["Members"] = int(soup.find("span",string="Members:").parent.text.replace("Members:","").replace(",","").strip())
            title_dict["Genres"] = [g.text for g in soup.find_all("span",itemprop="genre")]
            title_dict["Status"] = soup.find("span", string="Status:").parent.text.replace("Status:","").strip()
            for genre in self.mal_genres:
                title_dict[genre] = int(genre in title_dict["Genres"])

        return title_dict

    def titles_to_csv(self, file_path):
        df = pd.DataFrame(data=self.titles)
        df.to_csv(file_path, index=False)

    def load_from_csv(self, file_path):
        df = pd.read_csv(file_path)
        self.titles = df.to_dict("records")


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser("Scraper parser")
    arg_parser.add_argument('--start', type=int, required=False, default=0,
                            help="Number of first title scrapped, sorted by score")
    arg_parser.add_argument('--limit', type=int, required=False, default=1000,
                            help="Number of title at which scrapping stops, sorted by score")
    arg_parser.add_argument('--save', required=False, default="titles.csv",
                            help="Path to the file you want to save dataset into")
    arg_parser.add_argument('--load', required=False, default=None,
                            help="Path to the file with dataset you want to add data to")
    args = arg_parser.parse_args()
    mals = MALScraper()
    if args.load != None:
        mals.load_from_csv(args.load)
    mals.scrape_anime(args.start, args.limit)
    mals.titles_to_csv(args.save)
