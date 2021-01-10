import requests
import re
from bs4 import BeautifulSoup
from .config import Config

class My:

    def __init__(self):
        self.config = Config().fetch()
        self.name = None
        self.limit = None
        self.used = None
        self.left = None
        self.daily_limit = None
    
    def fetch(self):
        if self.__resolve() is True:
            return dict(
                username=self.name,
                limit=self.limit,
                daily_used=self.daily_limit,
                used=self.used,
                left=self.left
            )
        else:
            return None

    def __get(self):
        try:
            x = requests.get("https://vol.moe/my.php", cookies=self.config["account"], headers = {"user-agent": self.config["ua"]})
            return x.text
        except Exception as e:
            print("My: Connection Failed")
            print(e)
            return None
    
    def __resolve(self):
        html_text = self.__get()
        if html_text is not None:
            html = BeautifulSoup(html_text, "html.parser")

            username_html = html.select_one("#div_nickname_display")
            if username_html is not None:
                self.name = [text for text in username_html.stripped_strings][0]
                print("Username: ", self.name)

                bandwidth_html = html.select_one("#div_user_nor")
                bandwidth_text = [text for text in bandwidth_html.stripped_strings]
                self.daily_limit = float(re.search("(\d+(\.\d+)?)", bandwidth_text[3].split(",")[0]).group())
                print("Daily Used:", self.daily_limit, "M")
                self.used = float(re.search("(\d+(\.\d+)?)", bandwidth_text[3].split(",")[1]).group())
                print("Monthly Used:", self.used, "M")
                __temp = bandwidth_text[4].split(",")
                self.left = float(re.search("(\d+(\.\d+)?)", __temp[1]).group())
                print("Monthly Left:", self.left, "M")
                self.limit = float(re.search("(\d+(\.\d+)?)",__temp[0]).group())
                print("Monthly Limit:", self.limit, "M")

                return True
            else:
                print("My: Unable to login")
                return False

        return False
