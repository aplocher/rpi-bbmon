class FileWriter:
    def __init__(self, filename):
        self._filename = filename

    def write(self, text):
        file = open(self._filename, "w")
        file.write(text +"\n")
        file.close()