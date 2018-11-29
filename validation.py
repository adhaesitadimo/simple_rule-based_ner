from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import numpy as np


def get_true_entity_validation(morphemes, annot):
    annot_file = open(annot, 'r')
    entities = []
    for line in annot_file:
        entities += line.split('#')[1].strip().split(' ')
    true_vector = []
    pred_vector = []
    raw_words = []
    for sent in morphemes:
        for word in sent.split():
            pred_vector.append(0)
            raw_words.append(word)
            if word in entities:
                true_vector.append(1)
                entities = entities[1:]
            else:
                true_vector.append(0)
    return true_vector, pred_vector, raw_words


def quality_acess(true_vector, pred_vector):
    print('NER Precision: %.2f' % precision_score(true_vector, pred_vector))
    print('NER Recall: %.2f' % recall_score(true_vector, pred_vector))
    print('NER F1: %.2f' % f1_score(true_vector, pred_vector))
    print('NER ROC-AUC: %.2f' % roc_auc_score(true_vector, pred_vector))

    tpr, fpr, _ = roc_curve(true_vector, pred_vector)
    plt.plot(tpr, fpr)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid()
    plt.xticks(np.arange(0, 1.01, 0.1))
    plt.yticks(np.arange(0, 1.01, 0.1))
    plt.savefig('roc.jpg')