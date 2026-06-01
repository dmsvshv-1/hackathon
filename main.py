from classifier import Classifier

FILES = [
    "test_generated/t001.txt",
    "test_generated/t002.txt",
]

clf = Classifier().fit()
for file in FILES:
    category = clf.predict(file)
    print(f"{file} → {category}")
