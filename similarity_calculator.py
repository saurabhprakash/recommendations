import itertools
import multiprocessing


import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer

import data_processor


stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

dp = data_processor.DataProcessor()
data = dp.read_data_file()
response = {}


class SimilarityCalculator():
    """Similarity Calculator Logic, Calculates cosine similarity between the inputs
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(tokenizer=self.normalize, stop_words='english')

    def stem_tokens(self, tokens):
        return [stemmer.stem(item) for item in tokens]

    def normalize(self, text):
        """remove punctuation, lowercase, stem"""
        return self.stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

    def cosine_sim(self, text1, text2):
        tfidf = self.vectorizer.fit_transform([text1, text2])
        return ((tfidf * tfidf.T).A)[0, 1]

    def calculate_similarity(self, i1, i2):
        """Main method: which calculates similarity between various list elements"""
        i1 = data[i1]
        i2 = data[i2]
        key = i1['id'] + '_' + i2['id']
        sim = self.cosine_sim(i1['line'], i2['line'])
        response[key] = [
            sim,
            i1['line'],
            i2['line']
        ]

        f_h = open('highly_similar', 'w')
        try:
            if sim > 0.5:
                f_h.write('%s %s %s\n' % (sim, i1['line'].encode('utf8'), i2['line'].encode('utf8')))
        except UnicodeDecodeError:
            pass
        f_h.close()
        return True

def main(data):
    sm = SimilarityCalculator()
    size = len(data)
    with multiprocessing.Pool(initargs=(sm.calculate_similarity,)) as pool:
        for val in pool.starmap(sm.calculate_similarity, itertools.combinations(range(size), 2)):
            pass
        return

if __name__ == "__main__":
    main(data)



