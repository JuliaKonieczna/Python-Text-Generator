from nltk.tokenize import regexp_tokenize
from nltk import bigrams, trigrams
from collections import Counter
from random import choice, choices

PUNCTUATION = ".!?"


def get_tails_and_weights(word, ngram_dict):
    tails_frequency = Counter(ngram_dict.get(word))  # gets tail for 2-words head
    tails = [tail for tail in tails_frequency.keys()]
    weights = [weight for weight in tails_frequency.values()]
    return tails, weights


def generate_sentences(heads, ngram_dict):
    n = 2  # word counter, 2 words at the beginning
    word_pair = choice(heads)
    while (not word_pair[0].isupper()) or ((word_pair.split())[0][-1] in PUNCTUATION):
        word_pair = choice(heads)  # two words
    print(word_pair, end=" ")
    second_part = ((word_pair.split())[1])
    while True:
        tails, weights = get_tails_and_weights(word_pair, ngram_dict)  # gets tails and their weights for 2-words head
        try_word = ''.join(choices(tails, weights))  # gives the next word
        if len(tails) == 1 and try_word[-1] in PUNCTUATION and n >= 4:
            print(try_word)
            break
        elif try_word[-1] not in PUNCTUATION or (len(tails) == 1 and try_word[-1] in PUNCTUATION):
            word = try_word
            print(word, end=" ")
            n += 1
            word_pair = ' '.join([second_part, word])
            second_part = (word_pair.split())[1]
        elif try_word[-1] in PUNCTUATION and n >= 4:
            print(try_word)
            break


def find_frequency(tokenized_f, ngram_text, ngram_dict):
    while True:
        user_input = input()
        if user_input.lower() == "exit":
            break
        else:
            try:
                print(tokenized_f[int(user_input)])
                print(f'Head: {ngram_text[int(user_input)][0]} Tail: {ngram_text[int(user_input)][1]}')
                sorted_values = Counter(ngram_dict.get(user_input))
                print(f'Head: {user_input}')
                for value in sorted(sorted_values.items(), key=lambda x: x[1], reverse=True):
                    print(f'Tail: {value[0]} Count: {value[1]}')
            except TypeError:
                print("Type Error. Please input an integer.")
            except IndexError:
                print("Index Error. Please input an integer that is in the range of the corpus")
            except ValueError:
                print("Value Error. Invalid value.")
            except KeyError:
                print("Key Error. The requested word is not in the model. Please input another word.")
                continue
            finally:
                pass


def make_bigrams(tokenized_f):  # not used, trigrams are used to generate better sentences
    bigram_text = list(bigrams(tokenized_f))
    bigrams_dict = {}
    for bigram in bigram_text:
        bigrams_dict.setdefault(bigram[0], []).append(bigram[1])
    return bigrams_dict, bigram_text


def make_trigrams(tokenized_f):
    trigram_text = list(trigrams(tokenized_f))
    trigrams_dict = {}
    for trigram in trigram_text:
        head = ' '.join([trigram[0], trigram[1]])
        trigrams_dict.setdefault(head, []).append(trigram[2])
    trigram_heads = [head for head in trigrams_dict.keys()]
    return trigrams_dict, trigram_text, trigram_heads


def get_token_info(tokenized_f, ngram_text):
    print("Corpus statistics:")
    print(f'All tokens: {len(tokenized_f)}')
    print(f'Unique tokens: {len(set(tokenized_f))}')
    print(f'Number of ngrams: {len(ngram_text)}')


def main():
    while True:
        print("Please input file name with .txt")
        file_name = input()
        if ".txt" not in file_name:
            print("Please input file name with .txt")
        else:
            break
    with open(file_name, "r", encoding='utf-8') as f:
        read_f = f.read()
        tokenized_f = regexp_tokenize(read_f, '[^\s]+')
        ngram_dict, ngram_text, heads = make_trigrams(tokenized_f)
        for _ in range(10):
            generate_sentences(heads, ngram_dict)


if __name__ == "__main__":
    main()

