import re
import numpy as np

capital_reg = r'[А-ЯA-Z]+([а-яa-z]+)?'
surname = r'[A-Я][а-я]+((е|о|ё)в(а)?|(и|ы)н(а)?|(и|ы)(х|ч)|ий|ая|берг)$'
paternal = r'[A-Я][а-я]+((о|е)в(на|ич)|(ин)?ич(на)?)'


class RuleBasedNER:
    def __init__(self, sents, morphemes, vector):
        self.sents = sents
        self.morphemes = morphemes
        self.vector = vector
        self.names = []
        with open('name_gazetteer.txt', 'r') as name_gazetteer:
            for line in name_gazetteer:
                self.names.append(line.strip())
        self.orgs = []
        with open('org_gazetteer.txt', 'r') as org_gazetteer:
            for line in org_gazetteer:
                self.orgs.append(line.strip())
        self.locs = []
        with open('loc_gazetteer.txt', 'r') as loc_gazetteer:
            for line in loc_gazetteer:
                self.locs.append(line.strip())

    def is_capital(self, word, pos):
        if re.match(capital_reg, word) and pos != 0:
            return True
        else:
            return False

    def get_capital_words(self):
        coord = 0
        for sent in self.sents:
            for pos, word in enumerate(sent.split()):
                if self.is_capital(word, pos):
                    self.vector[coord] = 1
                coord += 1

    def is_name(self, word):
        if word in self.names or self.morphemes[word][-1].title() in self.names:
            return True
        else:
            return False

    def is_surname(self, word):
        if re.match(surname, word):
            return True
        else:
            return False

    def is_paternal(self, word):
        if re.match(paternal, word):
            return True
        else:
            return False

    def get_full_names(self):
        coord = 0
        for sent in self.sents:
            for pos, word in enumerate(sent.split()):
                if self.is_name(word) or self.is_surname(word) or self.is_paternal(word):
                    self.vector[coord] = 1
                coord += 1

    def get_window(self, sent, pos, width):
        if pos < width:
            return ' '.join(sent[:pos + width + 1])
        else:
            return ' '.join(sent[pos - width:pos + width + 1])

    def get_organization(self):
        coord = 0
        for sent in self.sents:
            sent_words = sent.split()
            for pos, word in enumerate(sent_words):
                if self.is_capital(word, pos):
                    window = self.get_window(sent_words, pos, 4).split()
                    for window_pos, item in enumerate(window):
                        if item in self.orgs:
                            self.vector[coord + window_pos - 4] = 1
                            nxt = 1
                            while True:
                                nxt += 1
                                if window_pos + nxt < len(window) - 1:
                                    if 'ADJF femn' in self.morphemes[window[window_pos + nxt]] or \
                                            'ADJF neut' in self.morphemes[window[window_pos + nxt]] or \
                                            'ADJF masc' in self.morphemes[window[window_pos + nxt]] or \
                                            'ADJF' in self.morphemes[window[window_pos + nxt]]:
                                        self.vector[coord + window_pos - 4 + nxt] = 1
                                    else:
                                        break
                                else:
                                    break
                coord += 1

    def get_location(self):
        coord = 0
        for sent in self.sents:
            sent_words = sent.split()
            for pos, word in enumerate(sent_words):
                if self.is_capital(word, pos):
                    window = self.get_window(sent_words, pos, 1).split()
                    for window_pos, item in enumerate(window):
                        if item in self.locs or self.morphemes[item][-1] in self.locs:
                            self.vector[coord + window_pos - 1] = 1
                coord += 1

