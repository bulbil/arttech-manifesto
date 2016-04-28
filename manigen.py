# -*- coding: UTF-8 -*-

# Random Text generator

from random import randint,choice
import nltk,re,json

SENT_END = ['.', '!', '?','--','...']
PUNC = ['.', '!', '?','--','...','`','\'',',']

def generate_manifesto(file_in):

    m = ManifestoGenerator(file_in)

    data = []

    for i in range(50):
        data.append(m.format_sentence(m.bigram_phrase()))
    for i in range(50):
        data.append(m.format_sentence(m.markov_phrase()))
    
    data = json.dumps(data, separators=(', ',': '),indent="\t")
    with open('data.json', 'w') as f:
        f.write(data)

    return 1


class ManifestoGenerator:

    def __init__(self,file_in):

        with open(file_in) as f:

            text = f.read()
            sents = nltk.sent_tokenize(text)
            sent_lengths = []

            for s in sents:
                curr_sent = nltk.word_tokenize(s)
                length = len(curr_sent)
                sent_lengths.append(length)

            self.tokens = nltk.word_tokenize(text)
            bigrams = nltk.bigrams(self.tokens)

            self.sent_lengths = sent_lengths
            self.cdf = nltk.ConditionalFreqDist(bigrams)

    def bigram_phrase(self):

        sentence = []
        curr_word = choice(self.tokens)
        sentence.append(curr_word)
        sent_length = choice(self.sent_lengths)
        for i in range(sent_length):

            index = 0
            curr_dist = self.cdf[curr_word]
            for i in curr_dist.values():
                if i < 5:
                    del curr_dist[index]
                    index += 1
                curr_word = choice(list(self.cdf[curr_word].keys()))
            sentence.append(curr_word)
        return sentence

    # def test_sentence_substrings(sentence, text, n=6):
        
    #     words = string.split(sentence)

    #     groups = [words[i:i+n] for i in range(0, len(words), n)]

    #     for group in groups:
    #         group = " ".join(group)
    #         if group in text:
    #             return False

    #     return True


    def markov_phrase(self):

        arr = []
        end_sentence = []
        dict = {}
        prev1 = ''
        prev2 = ''
        for word in self.tokens:
            if prev1 != '' and prev2 != '':
                key = (prev2, prev1)
                if key in dict:
                    dict[key].append(word)
                else:
                    dict[key] = [word]
                    if re.match("[\.\?\!]", prev1[-1:]):
                        end_sentence.append(key)
            prev2 = prev1
            prev1 = word

        if end_sentence == []:
            return

        key = ()
        sentence = []
        attempts = 0

        for i in range(choice(self.sent_lengths)):
            if key in dict:
                word = choice(dict[key])
                sentence.append(word)
                key = (key[1], word)
                if key in end_sentence:
                    # sentence_str = " ".join(sentence) 
                    
                    # check if the beginning of sentence occurs in the text
                    # if sentence_str[:15] not in phrase and sentence_str:

                    key = choice(end_sentence)
            else:
                key = choice(end_sentence)
                
        return sentence

    def format_sentence(self,sent_list):

        if sent_list[0] in PUNC:
            del sent_list[0]
        sent_list[0] = sent_list[0].title()
        sent_list = [v for v in sent_list if v != '.']
        sent_list = [v for v in sent_list if not v.isdigit()]
        while len(sent_list[-1]) < 5:
            sent_list[-1] = choice(self.tokens)
        sent_string = " ".join(sent_list)
        sent_string += choice(SENT_END)

        sent_string = re.sub(r'\s(,|;|\'|\"|\:)',r'\1',sent_string)
        sent_string = re.sub(r'(,|;|\'|\"|\:|`)+',r'\1',sent_string)
        return sent_string     


if __name__ == '__main__':

    generate_manifesto('arttech.txt')
