class BaseDocument(object):
    def __init__(self):
        self.text = []
        self.title = ""

    def add(self, text):
        self.text.append(text)
        return self

    def set_title(self, title):
        self.title = title
        return self
