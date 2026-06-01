class Statistika:
    def __init__(self):
        self.schetchik = {}
    def add_category(self, category):
        if category in self.schetchik:
            self.schetchik[category] += 1
        else:
            self.schetchik[category] = 1
    def show_status(self):
        print("Статистика по категориям:")
        for category, kolichestvo in self.schetchik.items():
            print(f"{category}: {kolichestvo}")


