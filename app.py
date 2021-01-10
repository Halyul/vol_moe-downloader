import requests
import os
import pathlib
import sys
import re
from lib.config import Config
from lib.my import My
from lib.myfollow import MyFollow
from lib.book import Book
from lib.history import History

class Downloader:

    def __init__(self):
        self.__my = My()
        self.__my_follow = MyFollow()
        self.__history = History()
        self.config = Config().fetch()
        self.account = None
        self.book_list = self.__my_follow.fetch()
        self.history = self.__history.fetch()
        self.download_queue = []
        self.downloading = None

    def start(self):
        # add download folder
        self.__make_dir(self.config["download_path"])
        # start download
        # book_list = [
        #     {'name': '五等分的花嫁', 'id': 52864, 'authors': ['春場ねぎ', '春場蔥'], 'last_update': '2020-11-14', 'is_finished': True}
        # ]
        # for book in book_list:
        for book in self.book_list:
            self.account = self.__my.fetch()
            # add book name folder
            self.__make_dir(self.config["download_path"] + "/" + book["name"])
            book_details = Book(book["id"]).fetch()
            self.__gen_queue(book_details)

            for item in self.download_queue:
                if self.__calc_limit(item) is False:
                    with open(os.path.join(item["file_path"], item["file_tmp"]), "wb") as f:
                        response = requests.get(item["download_link"], stream=True, allow_redirects=True, cookies=self.config["account"], headers = {"user-agent": self.config["ua"]})
                        total = response.headers.get("content-length")
                        self.downloading = item
                        print("Start Downloading:", item["file"])
                        if total is None:
                            f.write(response.content)
                        else:
                            downloaded = 0
                            total = int(total)
                            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                                downloaded += len(data)
                                f.write(data)
                                done = int(50*downloaded/total)
                                sys.stdout.write("\r[{}{}]".format("█" * done, "." * (50-done)))
                                sys.stdout.flush()
                    sys.stdout.write("\n")
                    self.__rename_file(os.path.join(item["file_path"], item["file_tmp"]), os.path.join(item["file_path"], item["file"]))
                    self.__history.add(item["book_name"], item["vol_name"])
                    print("Successfully downloaded:", item["file"])

                    self.account["left"] -= item["download_size"]
                    self.account["used"] += item["download_size"]
                    self.account["daily_used"] += item["download_size"]
                else:
                    print("Bandwidth limit excessed")
                    return
        
            self.__history.finished(book)
    
    def stop(self):
        if self.downloading is not None:
            try:
                os.remove(os.path.join(self.downloading["file_path"], self.downloading["file_tmp"]))
            except OSError:
                print ("\nDeletion of the file \"{}\" failed, it does not exist".format(self.downloading["file_tmp"]))
            else:
                print ("\nSuccessfully deleted the file \"{}\"".format(self.downloading["file_tmp"]))
        

    def __make_dir(self, pathname):
        path = os.path.join(pathlib.Path(__file__).parent.absolute(), pathname)
        try:
            os.makedirs(path)
        except OSError:
            print ("Creation of the directory \"{}\" failed, it already exists".format(path))
            return False
        else:
            print ("Successfully created the directory \"{}\"".format(path))
            return True

    def __gen_queue(self, book_details):
        for vol in book_details["vols"]:
            if self.__history.is_downloaded(book_details["book_name"], vol["vol"]) is False:
                filename = "{id}-{name}-{date}-{vol_name}".format(id=book_details["book_id"], name=book_details["book_name"], date=vol["date"], vol_name=vol["vol"])
                file_tmp = "{}.tmp".format(filename)
                file = "{filename}.{format}".format(filename=filename, format=self.config["type"])
                file_path = os.path.join(pathlib.Path(__file__).parent.absolute(), self.config["download_path"], book_details["book_name"])
                download_link = vol["link"]
                download_size = vol["size"]
                self.download_queue.append(dict(
                    file_tmp=file_tmp,
                    file=file,
                    file_path=file_path,
                    download_link=download_link,
                    download_size=download_size,
                    book_name=book_details["book_name"],
                    vol_name=vol["vol"]
                ))
        return

    def __rename_file(self, from_filename, to_filename):
        try:
            os.rename(from_filename, to_filename)
        except OSError:
            print ("Renaming the downloaded file failed")
        else:
            print ("Successfully renamed the downloaded file")
    
    def __calc_limit(self, item):
        is_excessed = True
        if self.account["left"] > item["download_size"] and self.account["used"] + item["download_size"] < self.account["limit"]:
            if self.account["daily_used"] + item["download_size"] < self.config["daily_limit"]:
                is_excessed = False
        return is_excessed

if __name__ == '__main__':
    d = Downloader()
    try: 
        d.start()
    except KeyboardInterrupt:
        d.stop()
        print("\nInterrupted, quit.")
    
