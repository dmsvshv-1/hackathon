import math  
import sys
import re  
from pathlib import Path  

TRAIN_LABELS_PATH = "example.txt"  
TRAIN_INBOX_DIR = "inbox"         
UNCLASSIFIED = "unclassified"  
CATEGORIES = ("critical_incident", "access_request", "software_issue", "hardware_issue","billing_docs", "hr_request", "monitoring", "meeting", "spam", UNCLASSIFIED,)

MODEL_CATEGORIES = ("critical_incident", "access_request", "software_issue", "hardware_issue","billing_docs", "hr_request", "monitoring", "meeting", "spam")

STOP_WORDS = { "a","an","and","best", "date", "data", "from", "grafana", "hi", "id", "internal", "komu", "kogo", "local", "noreply", "no", "org", "ot", "partner", "regards", "reply","ru","subject","tema", "the", "to","vendor", "with","а", "в","вам", "вас","вопрос", "во", "вложение", "дата", "день", "для", "добрый", "если", "заявки", "здравствуйте", "и","к", "код","коллеги", "кому","кого","на", "не", "но", "от", "отправлено", "пожалуйста", "по", "прикрепил", "привет", "с", "см",   "спасибо",  "теме", "тема", "у", "уважаемые","файл","что", "это"}


RULES = {
    "spam":             (("вы выиграли", 8.0), ("победителем розыгрыша", 8.0), ("банковской карты", 8.0), ("totally-not-spam", 8.0), ("secure-login-verify", 8.0), ("логин и пароль", 7.0), ("скидка 90", 7.0), ("только сегодня", 6.0), ("подтвердите личность", 5.0), ("пароль истекает", 5.0), ("перейдите по ссылке", 4.0), ("cdn-service.net", 10.0)),
    "critical_incident":(("критичный инцидент", 7.0), ("критический инцидент", 7.0), ("массовый сбой", 7.0), ("работа полностью остановлена", 12.0), ("работа остановлена", 12.0), ("ошибка 500", 5.0), ("у всех отдела", 10.0), ("несколько коллег", 10.0), ("не отвечает", 4.0), ("недоступен", 8.0), ("недоступна", 8.0), ("по-прежнему недоступ", 8.0), ("падает", 4.0), ("urgent", 2.0)),
    "access_request":   (("запрос доступа", 7.0), ("нужны права", 7.0), ("выдать доступ", 12.0), ("выдать права", 7.0), ("уровень доступа", 10.0), ("пропал доступ", 6.0), ("подготовить доступ", 6.0), ("новый сотрудник", 5.0), ("корпоративной почте", 4.0), ("права на", 4.0), ("права администратора", 6.0), ("доступ к", 3.0), ("восстановить", 3.0), ("vpn", 2.0), ("gitlab", 2.0), ("confluence", 2.0), ("1c", 2.0)),
    "software_issue":   (("внешний пользователь", 6.0), ("жалоба клиента", 6.0), ("клиент обращается повторно", 8.0), ("заявка висит без ответа", 8.0), ("нет ответа на тикет", 8.0), ("личным кабинетом", 5.0), ("клиент", 4.0), ("партнер", 4.0), ("api", 4.0), ("кнопка", 4.0), ("зарегистрироваться", 4.0), ("не запускается", 4.0), ("после обновления", 4.0), ("не открывает", 4.0), ("установщик", 4.0), ("ошибка при старте", 4.0), ("не могу установить", 4.0), ("chrome", 2.0), ("zoom", 2.0), ("excel", 2.0), ("outlook", 2.0), ("adobe", 2.0), ("антивирус", 2.0)),
    "hardware_issue":   (("неисправность оборудования", 8.0), ("заявку на ремонт", 7.0), ("диагностику или замену", 7.0), ("устройство", 5.0), ("не включается", 5.0), ("не определяется", 5.0), ("сломался", 5.0), ("ремонт", 4.0), ("замену", 4.0), ("принтер", 3.0), ("ноутбук", 3.0), ("гарнитура", 3.0), ("клавиатура", 3.0), ("мышь", 3.0), ("сканер", 3.0)),
    "billing_docs":     (("закрывающие документы", 8.0), ("счет", 6.0), ("акт", 5.0), ("оплата", 5.0), ("договор", 5.0), ("реквизит", 5.0), ("приложение к договор", 5.0), ("техническое задание", 4.0), ("финальная версия", 4.0), ("правки к", 4.0), ("инструкция на согласование", 14.0), ("принят в работу", 3.0)),
    "hr_request":       (("больнич", 7.0), ("отпуск", 7.0), ("график работы", 6.0), ("изменение графика", 6.0), ("изменить график работы", 6.0), ("график работы сотрудника", 6.0), ("период нетрудоспособности", 6.0), ("медицинским причинам", 6.0), ("кадровую систему", 6.0), ("кадровые данные", 5.0), ("будет отсутствовать", 5.0), ("bolnichnyy", 7.0), ("netrudosposobnosti", 7.0), ("grafika raboty", 5.0)),
    "monitoring":       (("плановый отчет мониторинга", 8.0), ("автоматическое уведомление", 8.0), ("сгенерировано автоматически", 8.0), ("disk usage", 7.0), ("cpu usage", 7.0), ("healthcheck", 6.0), ("uptime", 6.0), ("warning", 4.0), ("alert:", 7.0), ("корпоративный дайджест", 8.0), ("технические работы", 8.0), ("5xx", 6.0), ("среднее время ответа", 5.0)),
    "meeting":          (("нужен созвон", 9.0), ("созвон", 9.0), ("приглашение на демо", 10.0), ("демо новой версии", 10.0), ("предлагаю встретиться", 8.0), ("встретиться", 7.0), ("приглашение", 7.0), ("приглашаю", 7.0), ("статус задач", 8.0), ("подтвердите участие", 5.0), ("30 минут", 4.0), ("1 час", 4.0)),}

class Classifier:
    def __init__(self):
        self.category_docs = {}
        self.category_words = {}
        self.category_words_count = {}
        self.all_words = set()
        self.total_docs = 0

    def fit(self, labels_path=TRAIN_LABELS_PATH, inbox_dir=TRAIN_INBOX_DIR):
        inbox_dir = Path(inbox_dir)
        labels = self.load_labels(labels_path)

        self.category_docs = {}
        self.category_words = {}
        self.category_words_count = {}
        self.all_words = set()
        self.total_docs = 0

        for filename, category in labels.items():
            if category == UNCLASSIFIED:
                continue

            path = inbox_dir / filename
            text = self.read_text_file(path)
            if text is None:
                continue

            words = self.make_features(text)
            if not words:
                continue
            if category not in self.category_docs:
                self.category_docs[category] = 0
                self.category_words[category] = {}
                self.category_words_count[category] = 0

            self.category_docs[category] += 1
            for w in set(words):
                self.category_words[category][w] = self.category_words[category].get(w, 0) + words.count(w)
            self.category_words_count[category] += len(words)
            self.all_words.update(words)
            self.total_docs += 1
        return self

    def load_labels(self, labels_path):
        labels = {}
        with Path(labels_path).open(encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split()
                if len(parts) != 2:
                    raise ValueError(f"Bad label format at {labels_path}:{line_number}: {line!r}")

                filename, category = parts
                if category not in CATEGORIES:
                    raise ValueError(f"Unknown category {category!r} at {labels_path}:{line_number}")

                labels[filename] = category
        return labels

    def read_text_file(self, path):
        try:
            return Path(path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return None

    def normalize(self, text):
        text = text.lower().replace("ё", "е")
        text = re.sub(r"\b[\w.-]+@[\w.-]+\.\w+\b", " email ", text)
        text = re.sub(r"https?://\S+", " url ", text)
        text = text.replace("1с", "1c")
        text = text.replace("e-mail", "email")
        return text

    def get_tokens(self, text):
        return re.findall(r"[а-яa-z0-9_#]+", self.normalize(text))

    def is_good_token(self, token):
        if token in STOP_WORDS or len(token) <= 1 or token == "email":
            return False
        if token.isdigit() and token not in {"75", "80", "90", "401", "403", "404", "500"}:
            return False
        if token.startswith("#"):
            return False
        return True

    def make_features(self, text):
        tokens = [t for t in self.get_tokens(text) if self.is_good_token(t)]
        return tokens + [tokens[i] + "_" + tokens[i + 1] for i in range(len(tokens) - 1)]

    def predict(self, file_path):
        path = Path(file_path)
        if path.suffix.lower() != ".txt":
            return UNCLASSIFIED
        text = self.read_text_file(path)
        if text is None:
            return UNCLASSIFIED

        return self.predict_text(text)

    def predict_text(self, email):
        if not email.strip():
            return UNCLASSIFIED

        plain_tokens = [t for t in self.get_tokens(email) if self.is_good_token(t)]
        if self.is_vague(email, plain_tokens):
            return UNCLASSIFIED
        if self.total_docs == 0 or len(self.all_words) == 0:
            return UNCLASSIFIED

        scores = {}

        features = self.make_features(email)
        features_count = {w: features.count(w) for w in set(features)}
        alpha = 0.5
        vocab_size = len(self.all_words)

        categories_count = len(self.category_docs)
        for category in MODEL_CATEGORIES:
            if category not in self.category_docs:
                continue

            docs_in_category = self.category_docs[category]
            score = math.log((docs_in_category + 1) / (self.total_docs + categories_count))
            bottom = self.category_words_count[category] + alpha * vocab_size
            for word, count in features_count.items():
                top = self.category_words[category].get(word, 0) + alpha
                score += count * math.log(top / bottom)
            scores[category] = score
        normal_text = self.normalize(email)
        for category, phrases in RULES.items():
            for phrase, weight in phrases:
                if phrase in normal_text:
                    scores[category] = scores.get(category, 0.0) + weight
        return max(scores, key=scores.get)

    def is_vague(self, email, tokens):
        text = self.normalize(email)
        useful_tokens = [t for t in tokens if t not in {"re", "fwd", "fw"}]

        if "???" in text:
            return True
        if "см вложение" in text or "см. вложение" in text:
            return len(useful_tokens) < 12
        if "нужна помощь" in text:
            return len(useful_tokens) < 8
        if "не работает" in text and "уже второй день" in text:
            known_object = any(token in text for token in ("printer", "принтер", "ноутбук", "гарнитура", "мышь", "сканер", "vpn", "gitlab", "confluence", "active directory",))
            return not known_object
        return len(useful_tokens) < 4

if __name__ == "__main__":
    clf = Classifier().fit()
    for file_path in sys.argv[1:]:
        name = Path(file_path).name
        category = clf.predict(file_path)
        print(f"{name} send to → {category}")
