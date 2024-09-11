import re
from nltk.corpus import stopwords as sw
from nltk.stem import WordNetLemmatizer
from cran_reader import Document
from typing import List

# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

class Indexing:
    def __init__(self):

        self.inverted_index = {} # key: word, value: list of tuples (docno, count)
        self.document_vectors = {} # key: docno, value: dictionary of word frequency
        self.document_frequency = {} # key: word, value: document frequency
        self.avg_doc_length = 0
        self.corpus_size = 0

        self.token_pattern = re.compile(r"\b\w{2,}\b")
        self.stopwords = set(sw.words('english'))
        self.lemmetizer = WordNetLemmatizer()

    def process_text(self, text): 
        # Creating tokens from the text  
        temp = self.token_pattern.findall(text.lower())    

        # Removing stopwords  
        temp = [x for x in temp if x not in self.stopwords]

        # Performing stemming operation
        # temp = [self.stemmer.stem(x) for x in temp]

        # Performing lemmetization operation
        temp = [self.lemmetizer.lemmatize(x) for x in temp]
        return temp

    def build_index(self, documents: List[Document]):
        self.total_documents = len(documents)

        for i, doc in enumerate(documents):
            # Selecting the text to be indexed
            document_fields = [item for item in [doc.title, doc.author, doc.bib, doc.text] if item is not None]
            tokens = self.process_text(" ".join(document_fields))

            # Checking duplicate documents
            if doc.docno in self.document_vectors:
                raise ValueError(f"[DUPLICATE DOCUMENT FOUND] - Document {doc.docno} already exists in the index.")

            # Calculating the word frequency for each document
            word_vector = {}
            for word in tokens:
                word_vector[word] = word_vector.get(word, 0) + 1

            # Creating the inverted index and document frequency
            for word, freq in word_vector.items():
                if self.inverted_index.get(word) is None:
                    self.inverted_index[word] = []
                self.inverted_index[word].append((doc.docno, freq))

                # Calculating the document frequency for each word
                self.document_frequency[word] = self.document_frequency.get(word, 0) + 1

                self.corpus_size += freq

            self.document_vectors[doc.docno] = word_vector
        
            print(f"Indexing... ({i + 1} / {len(documents)})", end="\r")

        # Calculating some stats
        self.avg_doc_length = self.corpus_size / self.total_documents
        print("\nIndexing completed.")

    def get_document_list(self, query_terms):
        """
        Get the list of documents from inverted_index for the given query terms
        """
        document_list = set()
        for term in query_terms:
            if term in self.inverted_index:
                document_list.update([x[0] for x in self.inverted_index[term]])
        return document_list
