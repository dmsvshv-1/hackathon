import shutil
import os
class Movver:
    def __init__(self, destination):
        self.destination = destination
    def move(self, pismo, category):
        papka = os.path.join(self.destination, category)
        os.makedirs(papka, exist_ok=True)
        shutil.move(pismo, papka)
    def move_all(self, example_file):
        with open(example_file, encoding='utf-8') as f:
            for stroka in f:
                slova = stroka.strip().split()
                filename = slova[0]
                category = slova[-1]
                self.move('inbox/' + filename, category)
            