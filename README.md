# Document Search Engine Using Vector Representations

This application is designed to enable efficient document retrieval through vector-based representation methods. The core functionalities include:

- Adding a text document ✅  
- Searching using a query input ✅

---

## Features and Workflow

### A. Preprocessing of Documents and Queries ✅
- **Tokenization:** Splitting the text into individual words or tokens.  
- **Normalization:** Removing special characters, converting all text to lowercase, eliminating stop words, etc.  
- **Stemming or Lemmatization:** Reducing words to their base or root forms for uniformity.

### B. Vectorization Using Two Methods ✅
- **TF-IDF:**  
  - The initial document corpus serves as the dictionary.  
  - The dictionary can be dynamically updated as the corpus grows.  
- **Word Embeddings (Word2Vec, GloVe, or similar):**  
  - Both documents and queries are represented as the sum of individual word embeddings.

### C. Similarity Calculation and Ranking ✅
- **Similarity Metric:** At least cosine similarity is used to measure the closeness between vectors.  
- **Ranking:** Documents are sorted from the most similar (smallest distance) to the least similar relative to the query.

### D. Results Analysis ✅
- The report presents examples of search results obtained using both vectorization methods, along with a subjective evaluation of their effectiveness.

---

This approach ensures a robust and scalable document retrieval system, combining classical statistical methods with modern word embedding techniques.
