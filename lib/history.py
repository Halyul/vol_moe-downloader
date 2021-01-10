import os
import pathlib
import yaml

class History:

    def __init__(self):
        self.path = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "history.yml")
        self.history = yaml.safe_load(open(self.path, "r"))
    
    def fetch(self):
        return self.history
    
    def add(self, book, vol):
        if book in self.history:
            if vol in self.history[book]:
                return False
            else:
                self.history[book].append(vol)
        else:
            self.history[book] = []
            self.history[book].append(vol)
        
        self.__dump()
        return True
    
    def remove(self, book, vol):
        if book in self.history:
            if vol in self.history[book]:
                self.history[book].remove(vol)
                if len(self.history[book]) == 0:
                    self.history.pop(book)
                self.__dump()
                return True
        
        return False
    
    def is_downloaded(self, book, vol):
        if self.history is not None:
            if book in self.history:
                if self.history[book] == "all":
                    return True
                else:
                    if vol in self.history[book]:
                        return True
        else:
            self.history = {}
        
        return False

    def finished(self, book_details):
        if book_details["is_finished"] is True:
            self.history[book_details["name"]] = "all"
            self.__dump()
        return

    def __dump(self):
        with open(self.path, "w") as f:
            yaml.safe_dump(self.history, f, allow_unicode=True)