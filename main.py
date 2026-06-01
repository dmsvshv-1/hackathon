from email_reader import EmailReader
from classifier import Classifier
from movver import Movver
from loggger import Loggger
from statistika import Statistika

chitatel = EmailReader('inbox')
klassifikator = Classifier()
perekladyvatel = Movver('processed')
dnevnik = Loggger('logs/run.log')
schetchik = Statistika()

pisma = chitatel.read()

for pismo in pisma:
    catagory = klassifikator.classify(pismo.body)
    perekladyvatel.move('inbox/' + pismo.name, catagory)
    dnevnik.log(pismo.name + '-' + catagory)
    schetchik.add_category(catagory)
schetchik.show_status()
