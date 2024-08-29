import requests
from parsel import Selector


class HouseKGParsel:
    main_url = 'https://www.house.kg/snyat'
    base_url = "https://www.house.kg"

    def get_page(self):
        page = requests.get(url=HouseKGParsel.main_url, timeout=10)
        self.page = page.text

    def get_house_links(self):
        html = Selector(text=self.page)
        links = html.css("div.listings-wrapper div.listing meta[itemprop='url']::attr(content)").getall()
        full_links = [self.base_url + link for link in links]
        return full_links[:2]


if __name__ == "__main__":
    crawler = HouseKGParsel()
    crawler.get_page()
    crawler.get_house_links()
    for link in crawler.get_house_links():
        print(link)

