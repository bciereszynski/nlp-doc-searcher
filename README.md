[PL]
```
Wyszukiwarka dokumentów z wykorzystaniem reprezentacji wektorowej.
Aplikacja powinna umożliwiać:
● Dodanie dokumentu tekstowego ✅
● Wyszukiwanie za pomocą zapytania ✅

A. Dokumenty i zapytania powinny być wstępnie przetworzone: ➕
● Tokenizacja - podział tekstu na słowa/tokeny. ✅
● Normalizacja - usunięcie znaków specjalnych, zamiana na małe litery, ✅
usunięcie stop-słów itp. ✅
● Stemming lub lematyzacja - redukcja słów do ich podstawowych form. ✅
B. Następnie zwektoryzowane dwoma metodami:
● Tf-idf, wstępna baza dokumentów służy za słownik, dodatkowo wraz ze
wzrostem bazy słownik może być przebudowany ✅
● Word2vec lub GloVe lub inny podobny model, dokument i zapytanie jest
reprezentowane jako suma embeddingów poszczególnych słów
C. Obliczenie podobieństwa:
● Przynajmniej podobieństwo cosinusowe ✅
● Posortowanie dokumentów od najbardziej podobnych do zapytania (tych
z najmniejsza odległością) do tych najmniej podobnych
D. Analiza wyników:
● W sprawozdaniu pokazanie kilku wyników z dwoma metodami
wektoryzacji i ich subiektywna ocena.
```

To download spacy language model:

python -m spacy download en_core_web_sm
