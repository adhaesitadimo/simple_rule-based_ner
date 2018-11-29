from preprocessing import graphemic, morphologic
from validation import get_true_entity_validation, quality_acess
from rules import RuleBasedNER
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser(description='Simple rule-based Named Entity Recognition modeule')
    parser.add_argument('text', help='path to raw .txt file for named entity recognition')
    parser.add_argument('objects', help='true objects markup for validation')
    args = parser.parse_args()

    tokens = graphemic(args.text)
    morphemes, sents = morphologic(tokens)
    true_vector, pred_vector, raw_words = get_true_entity_validation(sents, args.objects)
    ner = RuleBasedNER(sents, morphemes, pred_vector)
    ner.get_capital_words()
    ner.get_full_names()
    ner.get_organization()
    ner.get_location()
    quality_acess(true_vector, pred_vector)

    print('--------------------------------')
    for true, pred, word in zip(true_vector, pred_vector, raw_words):
        if true != pred:
            if true == 1:
                print('Missed named entity part: %s' % word)
            else:
                print('Falsely identified named entity part: %s' % word)