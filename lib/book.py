import requests
import re
from bs4 import BeautifulSoup
from lib.config import Config

class Book:

    def __init__(self, id):
        self.config = Config().fetch()
        self.id = id

    def fetch(self):
        return self.__resolve()
    
    def __get(self):
        try:
            x = requests.get("https://vol.moe/c/{}.htm".format(self.id), cookies=self.config["account"], headers = {"user-agent": self.config["ua"]})
            return x.text
        except Exception as e:
            print("Book: Connection Failed")
            print(e)
            return None
    
    def __resolve(self):
        html_text = self.__get()
        if html_text is not None:
            html = BeautifulSoup(html_text, "html.parser")

            if self.config["type"] == "mobi":
                vol_list_html = html.select_one("#div_mobi")
            else:
                vol_list_html = html.select_one("#div_cbz")

            dates_names_html = html.select_one("#div_mobi").select("b[title]") # get status
            file_sizes_text = [[text for text in item.stripped_strings][0] for item in vol_list_html.select("font[class='filesize']")]
            file_sizes = []

            for item in file_sizes_text:
                r = re.search("(\d+(\.\d+))", item)
                if r is not None:
                    file_sizes.append(r.group())

            download_links = [download_link_html["href"] for download_link_html in vol_list_html.select("a[href]") if download_link_html.string == "下載"]

            book_details = dict(
                        book_name=[text for text in html.select_one("td[class='author']").select_one("font[class='font_big']").stripped_strings][0],
                        book_id=self.id,
                        vols=[]
            )

            for i in range(len(download_links)):
                if download_links[i].find("javascript:") == -1:
                    item = dict(
                        link=download_links[i],
                        date=dates_names_html[i]["title"],
                        vol=dates_names_html[i].string.strip(),
                        size=float(file_sizes[i])
                    )
                    book_details["vols"].append(item)
                else:
                    print("Downloader: Unable to login")
                    return None
            
            return book_details
        
        return None
            