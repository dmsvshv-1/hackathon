import re
class Classifier:
    def __init__(self):
        self.example = {}
        self.words = {}
        self.stop_word = {'subject','from','to','date','от','кого','кому','дата','тема'}
        self.freqancy = {}
        
        with open("example.txt", encoding = 'utf-8') as f:
            for line in f:
                parts = line.strip().split()
                filename = parts[0]
                category = parts[1]
                self.example[filename] = category
                
        for filename,category in self.example.items():
            with open("inbox/"+filename, encoding = 'utf-8') as g:
                text = g.read()
                token = [i for i in self.tokenizer(text) if i not in self.stop_word]
                if category not in self.words:
                    self.words[category] = token
                else:
                    self.words[category].extend(token)

        for category, word in self.words.items():
            self.freqancy[category] = self.give_value_words(word)
                    
    def tokenizer(self, text):
        return re.findall(r'[а-яёa-z]+',text.lower())
    
    def give_value_words(self,words_in_categpry):
        earn_words = {}
        for i in words_in_categpry:
            words_weight = words_in_categpry.count(i)/len(words_in_categpry)
            earn_words[i] = words_weight
        return earn_words
    
    def classify(self,email):
        tokens = [i for i in self.tokenizer(email) if i not in self.stop_word]
        email_value = self.give_value_words(tokens)
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
                    

                
            
            
        
            
        
                
        