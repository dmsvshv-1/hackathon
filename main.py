import os
from classifier import Classifier
from movver import Movver
from loggger import Loggger
from statistika import Statistika

# создаём и обучаем классификатор
klassifikator = Classifier().fit()

perekladyvatel = Movver('processed')
dnevnik = Loggger('logs/run.log')
schetchik = Statistika()

# идём по всем файлам в папке inbox
for filename in os.listdir('inbox'):
    path = 'inbox/' + filename
    if not os.path.isfile(path):
        continue

    # классификатор сам читает файл и выдаёт категорию
    catagory = klassifikator.predict(path)

    perekladyvatel.move(path, catagory)
    dnevnik.log(filename + ' -> ' + catagory)
    schetchik.add_category(catagory)

schetchik.show_status()