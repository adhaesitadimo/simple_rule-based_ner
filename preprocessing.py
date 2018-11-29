from nltk import sent_tokenize, word_tokenize
import pymorphy2


def graphemic(text_file):
    txt = open(text_file, "r")
    text = ''
    for line in txt:
        text += line
    sents = sent_tokenize(text)
    sent_tokens = [word_tokenize(s) for s in sents]
    txt.close()
    return sent_tokens


def morphologic(token_sents):
    raw_morph_text = []
    morph = pymorphy2.MorphAnalyzer()
    morphemes = {}
    for sent in token_sents:
        raw_sent = ''
        for token in sent:
            #print(token)
            #print(type(morph.parse(token)[0][1]))
            if str(morph.parse(token)[0][1]) != 'PNCT':
                morphemes[token] = str(morph.parse(token)[0][1]).split(',') + [morph.parse(token)[0][2]]
                raw_sent += token + ' '
        raw_morph_text.append(raw_sent)
    return morphemes, raw_morph_text



