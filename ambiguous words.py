import nltk
from nltk.corpus import wordnet as wn
nltk.download('wordnet')

def get_ambiguous_words(min_senses=3, max_words=300):
    words = set()
    for synset in list(wn.all_synsets('n')):
        lemma_names = synset.lemma_names()
        for lemma in lemma_names:
            senses = wn.synsets(lemma)
            if len(senses) >= min_senses:
                words.add(lemma.lower())
            if len(words) >= max_words:
                return sorted(words)
    return sorted(words)
ambiguous_list = get_ambiguous_words()
print("Ambiguous Words List:")
print(ambiguous_list)