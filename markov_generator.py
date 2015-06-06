import random
from collections import defaultdict


class MarkovGenerator(object):

    def __init__(self, corpus, tuple_size=3):
        """ Initialize the MarkovGenerator object.

        Digests the corpus of text provided as a list of tokens and creates a cache of
        predicted next-word values

        Code for markov generator based on:  http://agiliq.com/blog/2009/06/
        generating-pseudo-random-text-with-markov-chains-u/

        :param corpus: (list) a source text of word tokens to generate random text from
        :param tuple_size: (int: default 3)
        :return: None
        """
        self.corpus = corpus
        self.corpus_size = len(corpus)

        self.tuple_size = tuple_size
        self.cache = defaultdict(list)
        self._initialize_cache()

    def _generate_ngrams(self):
        """ Generate ngrams from the corpus

        For each token in the corpus, generate a list of likely next words for the
        Markov text generator to return.

        :yield: (tuple) a tuple of length n
        """
        n = self.tuple_size

        if len(self.corpus) < n:
            return

        for i in range(len(self.corpus) - (n - 1)):
            yield tuple([self.corpus[i + x] for x in range(n)])

    def _initialize_cache(self):
        """ Initialize the cache

        Set up the cache object to generate predicted strings.

        :return: None
        """
        for word_tuple in self._generate_ngrams():
            self.cache[word_tuple[0:-1]].append(word_tuple[-1])

    def generate_markov_text(self, size, override_seed=None):
        """ Generate a pseudo-random block of text

        :param size: (int) Length of text to generate. Should be << than the
                     size of the total corpus for good results.
        :param override_seed: (str: default None) Word to seed the generator
                               with if set.
        :return: (str) a string of randomly-generated text
        """

        if not override_seed:
            seed = random.randint(0, self.corpus_size - self.tuple_size)
        else:
            indices = [i for i, x in enumerate(self.corpus) if x == override_seed]
            try:
                seed = random.choice(indices)
            except IndexError:
                seed = random.randint(0, self.corpus_size - self.tuple_size)

        seed_words = self.corpus[seed: seed + self.tuple_size]
        gen_words = []

        for i in xrange(size):
            gen_words.append(seed_words[0])
            seed_words.pop(0)
            try:
                seed_words.append(random.choice(self.cache[tuple(seed_words)]))
            # catch cases where there isn't a word to pick
            except IndexError:
                seed_words.append(random.choice(self.corpus))

        gen_words.append(seed_words[0])

        return ' '.join(gen_words)
