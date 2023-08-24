import itertools
import os
import logging
import numpy as np
import pandas as pd
from scipy.stats import entropy

pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_rows', None)  # 显示所有行

DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "data",
)

log = logging.getLogger()
MISS = np.uint8(0)
MISPLACED = np.uint8(1)
EXACT = np.uint8(2)

SHORT_WORD_LIST_FILE = os.path.join(DATA_DIR, "possible_words.txt")
LONG_WORD_LIST_FILE = os.path.join(DATA_DIR, "allowed_words.txt")
PATTERN_MATRIX_FILE = os.path.join(DATA_DIR, "pattern_matrix.npy")
MCM_FILE = os.path.join(DATA_DIR, "mcm_matrix.npy")
# To store the large grid of patterns at run time
PATTERN_GRID_DATA = dict()


# Generating color patterns between strings, etc.
def words_to_int_arrays(words):
    return np.array([[ord(c) for c in w] for w in words], dtype=np.uint8)


def generate_pattern_matrix(words1, words2):
    """
    A pattern for two words represents the wordle-similarity
    pattern (grey -> 0, yellow -> 1, green -> 2) but as an integer
    between 0 and 3^5. Reading this integer in ternary gives the
    associated pattern.

    This function computes the pairwise patterns between two lists
    of words, returning the result as a grid of hash values. Since
    this can be time-consuming, many operations that can be been vectorized
    (perhaps at the expense of easier readability), and the result
    is saved to file so that this only needs to be evaluated once, and
    all remaining pattern matching is a lookup.
    """

    # Number of letters/words
    nl = len(words1[0])
    nw1 = len(words1)  # Number of words
    nw2 = len(words2)  # Number of words

    # Convert word lists to integer arrays
    word_arr1, word_arr2 = map(words_to_int_arrays, (words1, words2))

    # equality_grid keeps track of all equalities between all pairs
    # of letters in words. Specifically, equality_grid[a, b, i, j]
    # is true when words[i][a] == words[b][j]
    equality_grid = np.zeros((nw1, nw2, nl, nl), dtype=bool)
    for i, j in itertools.product(range(nl), range(nl)):
        equality_grid[:, :, i, j] = np.equal.outer(word_arr1[:, i], word_arr2[:, j])
        """
        A pattern for two words represents the wordle-similarity
        pattern (grey -> 0, yellow -> 1, green -> 2) but as an integer
        between 0 and 3^5. Reading this integer in ternary gives the
        associated pattern.

        This function computes the pairwise patterns between two lists
        of words, returning the result as a grid of hash values. Since
        this can be time-consuming, many operations that can be been vectorized
        (perhaps at the expense of easier readability), and the result
        is saved to file so that this only needs to be evaluated once, and
        all remaining pattern matching is a lookup.
        """
    # full_pattern_matrix[a, b] should represent the 5-color pattern
    # for guess a and answer b, with 0 -> grey, 1 -> yellow, 2 -> green
    full_pattern_matrix = np.zeros((nw1, nw2, nl), dtype=np.uint8)

    # Green pass
    for i in range(nl):
        matches = equality_grid[:, :, i, i].flatten()  # matches[a, b] is true when words[a][i] = words[b][i]
        full_pattern_matrix[:, :, i].flat[matches] = EXACT
        """
        full_pattern_matrix[:, :, i] circulate all pattern-comparing pairs in the words1 x words2 on 'i' digit.
        full_pattern_matrix[:, :, i].flat[matches] = EXACT makes the perfect fitting digit in pattern matrix get a '2'
        """
        for k in range(nl):
            # If it's a match, mark all elements associated with
            # that letter, both from the guess and answer, as covered.
            # That way, it won't trigger the yellow pass.
            equality_grid[:, :, k, i].flat[matches] = False
            equality_grid[:, :, i, k].flat[matches] = False

    # Yellow pass
    for i, j in itertools.product(range(nl), range(nl)):
        matches = equality_grid[:, :, i, j].flatten()
        full_pattern_matrix[:, :, i].flat[matches] = MISPLACED
        """
        full_pattern_matrix[:, :, i].flat[matches] = MISPLACED makes the random fitting digit in pattern matrix get a '1'
        """
        for k in range(nl):
            # Similar to above, we want to mark this letter
            # as taken care of, both for answer and guess
            equality_grid[:, :, k, j].flat[matches] = False
            equality_grid[:, :, i, k].flat[matches] = False

    # Rather than representing a color pattern as a lists of integers,
    # store it as a single integer, whose ternary representations corresponds
    # to that list of integers.

    pattern_matrix = np.dot(
        full_pattern_matrix,
        (3 ** np.arange(nl)).astype(np.uint8)
    )

    return pattern_matrix


def get_word_list(short=False):
    result = []
    file = SHORT_WORD_LIST_FILE if short else LONG_WORD_LIST_FILE
    with open(file) as fp:
        result.extend([word.strip() for word in fp.readlines()])
    return result


def generate_full_pattern_matrix():
    words = get_word_list()
    pattern_matrix = generate_pattern_matrix(words, words)
    # Save to file
    np.save(PATTERN_MATRIX_FILE, pattern_matrix)
    return pattern_matrix


def get_pattern_matrix(words1, words2):
    if not PATTERN_GRID_DATA:
        if not os.path.exists(PATTERN_MATRIX_FILE):
            log.info("\n".join([
                "Generating pattern matrix. This takes a minute, but",
                "the result will be saved to file so that it only",
                "needs to be computed once.",
            ]))
            generate_full_pattern_matrix()
        PATTERN_GRID_DATA['grid'] = np.load(PATTERN_MATRIX_FILE)
        PATTERN_GRID_DATA['words_to_index'] = dict(zip(
            get_word_list(), itertools.count()
        ))

    full_grid = PATTERN_GRID_DATA['grid']
    words_to_index = PATTERN_GRID_DATA['words_to_index']

    indices1 = [words_to_index[w] for w in words1]
    indices2 = [words_to_index[w] for w in words2]
    return full_grid[np.ix_(indices1, indices2)]


# Functions associated with entropy calculation


def get_weights(words, priors):
    frequencies = np.array([priors[word] for word in words])
    total = frequencies.sum()
    if total == 0:
        return np.zeros(frequencies.shape)
    return frequencies / total


def get_pattern_distributions(allowed_words, possible_words, weights):
    """
    For each possible guess in allowed_words, this finds the probability
    distribution across all the 3^5 wordle patterns you could see, assuming
    the possible answers are in possible_words with associated probabilities
    in weights.

    It considers the pattern hash grid between the two lists of words, and uses
    that to bucket together words from possible_words which would produce
    the same pattern, adding together their corresponding probabilities.
    """
    pattern_matrix = get_pattern_matrix(allowed_words, possible_words)

    n = len(allowed_words)
    distributions = np.zeros((n, 3 ** 5))
    #print('-------------------------------')
    #print(distributions)
    n_range = np.arange(n)
    #print(n_range)
    for j, prob in enumerate(weights):
        '''
        print('1+++++++++++++')
        print(n_range)
        print('2+++++++++++++')
        print(pattern_matrix[:, j])
        print('3+++++++++++++')
        print(distributions[n_range, pattern_matrix[:, j]])
        '''
        distributions[n_range, pattern_matrix[:, j]] += prob
        # print('4+++++++++++++')
        # print(distributions[n_range, pattern_matrix[:, j]])
    # print('-------------------------------')
    return distributions


#allowed_words = get_word_list()
allowed_words = ['mummy', 'slate']
possible_words = get_word_list(short=True)
# possible_words = ['hello', 'sorry', 'annoy', 'apple']
weights = np.ones(len(possible_words)) / len(possible_words)
#print(weights)
pattern_matrix = get_pattern_matrix(allowed_words, possible_words)
distri = get_pattern_distributions(allowed_words, possible_words, weights)
counts = get_pattern_distributions(allowed_words, possible_words, np.ones(len(possible_words)))
#print(distri)


def entropy_of_distributions(distributions, atol=1e-12):
    axis = len(distributions.shape) - 1
    return entropy(distributions, base=2, axis=axis)


def get_entropies(allowed_words, possible_words, weights):
    if weights.sum() == 0:
        return np.zeros(len(allowed_words))
    distributions = get_pattern_distributions(allowed_words, possible_words, weights)
    return entropy_of_distributions(distributions)


entropy_result = get_entropies(allowed_words, possible_words, weights)
print(entropy_result)


df = pd.DataFrame(distri)
df.to_excel(r"C:\Users\Administrator\Desktop\2023File\2023_MCM-ICM_Problems\CalEntropies.xlsx", sheet_name='Sheet1',
            index=False)

def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')
