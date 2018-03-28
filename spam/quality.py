from os import path
from confmat import BinaryConfusionMatrix
from utils import read_classification_from_file as rcff
'''Used to evaluate quality of filter output'''
def compute_quality_for_corpus(directory):
    truths = path.join(directory, "!truth.txt")
    predicts = path.join(directory, "!prediction.txt")
    matrix = BinaryConfusionMatrix()
    matrix.compute_from_dicts(rcff(truths), rcff(predicts))
    #print("False negatives: ", matrix.fn)
    #print("False positives: ", matrix.fp)
    return matrix.quality_score()
    
if __name__=="__main__":
    print("Score: ", compute_quality_for_corpus("./emails/1/"))