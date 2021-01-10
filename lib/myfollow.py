import requests
from bs4 import BeautifulSoup
from .config import Config

class MyFollow:

    def __init__(self):
        self.config = Config().fetch()
        self.follow = list()

    def fetch(self):
        if self.__resolve() is True:
            return self.follow
        else:
            return None

    def __get(self):
        try:
            x = requests.get("https://vol.moe/myfollow.php", cookies=self.config["account"], headers = {"user-agent": self.config["ua"]})
            return x.text
        except Exception as e:
            print("MyFollow: Connection Failed")
            print(e)
            return None

    def __resolve(self):
        html_text = self.__get()
        if html_text is not None:
            html = BeautifulSoup(html_text, "html.parser")

            booklist_html = html.select_one("table[class='book_list']")

            if booklist_html is not None:
                books_html = booklist_html.select("a[target='_blank']")
                for book_html in books_html:
                    book_item_html = book_html.parent.parent.select("td")
                    is_finished_tmp = [text for text in book_item_html[5].stripped_strings]
                    if is_finished_tmp[0] != is_finished_tmp[-1]:
                        is_finished = True
                    else:
                        is_finished = False
                    item = dict(
                        name=book_item_html[1].select_one("a").string,
                        id=int(book_item_html[0].string),
                        authors=book_item_html[2].string.strip().split(","),
                        last_update=book_item_html[4].string.strip(),
                        is_finished=is_finished
                    )
                    self.follow.append(item)

                return True
            else:
                print("MyFollow: Unable to login")
                return False

        return False