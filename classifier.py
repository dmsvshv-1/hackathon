import re
class Classifier:
    def __init__(self):
        self.example = {} #я создал файл example где по первым 20 файлам каждый закинул в определенную группу типо software_issue все в файле example.txt
        self.words = {} #список группа:слова которые туда входят и схожие на эту группу
        self.stop_word = {'subject','from','to','date','от','кого','кому','дата','тема'} #это слова которые не влияют на распределние на категорию письма(потом я их не учитываю)
        self.freqancy = {}
        
        with open("example.txt", encoding = 'utf-8') as f: #тут я открваю файл с который я сам руками распределили по категориям как пример там написно так "mail_0001.txt software_issue"
            for line in f:
                parts = line.strip().split()#разделяю строку mail_0001.txt software_issue по пробелам и убераю все точки и так далее
                filename = parts[0]# первое слово название письма
                category = parts[1]# его категория
                self.example[filename] = category #закидываю в словарь как mail_0001.txt:software_issue
                
        for filename,category in self.example.items(): 
            with open("inbox/"+filename, encoding = 'utf-8') as g:#открываю файлы из example через через inbox
                text = g.read()#читаю содержимое
                token = [i for i in self.tokenizer(text) if i not in self.stop_word] #разбиваю слова через фунцию tokenizer(снизу опишу что она делает)и если этого слова нету в стоп словах(выше словарь)
                if category not in self.words: #если категория уже есть в списке то закидываем слово к нужной категории
                    self.words[category] = token
                else:
                    self.words[category].extend(token)#делаем новую группу слов и закидываем слово туда 

        for category, word in self.words.items():
            self.freqancy[category] = self.give_value_words(word)#тут мы слово даем его ценность(токен в виде числа типо 0.33 то есть слово:0.33)
                    
    def tokenizer(self, text):
        return re.findall(r'[а-яёa-z]+',text.lower()) #тут мы текст ращбиваем на слова6делаем все буквы маленькие,убираем все знаки6пробелмы и т.д получаем список просто слов из письма
    
    def give_value_words(self,words_in_category):# тут мы даем слову его ценность,делаем мы это так:сколько раз слово встречается в определенной группе/ на все слова в группе
        earn_words = {} #словарь где будет слово:его значение
        for i in words_in_category:
            words_weight = words_in_category.count(i)/len(words_in_category)#считаем ценность слова по формуле
            earn_words[i] = words_weight #закидываем слово в слоарь слово:ценность
        return earn_words
    
    def classify(self,email):#тут мы классифицируем уже слова из письма все что выше это мы эталонные слова раскидвали из первых 20 писем в словари чтобы потом по ним ориентироваться для обработки письма
        tokens = [i for i in self.tokenizer(email) if i not in self.stop_word] # разбиваем текст без стоп слов (они в словаре выше) без точек и всех знаков,через функцию tokenizer
        email_value = self.give_value_words(tokens)#даем каждому слову его ценность
        best_score = 0
        best_category = 'unclassified'
        for category, freqenc in self.freqancy.items():
            score = 0
            for word_email in email_value:
                if word_email in freqenc:
                    score += email_value[word_email]*freqenc[word_email]
                if score>best_score:
                    best_score = score
                    best_category = category
        return best_category
                    

                
            
            
        
            
        
                
        