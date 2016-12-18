
class BinaryConfusionMatrix(object):
    def __init__(self, pos_tag="OK", neg_tag="SPAM"):
        self.tp = 0
        self.tn = 0
        self.fp = 0
        self.fn = 0
        
        self.pos_tag = pos_tag
        self.neg_tag = neg_tag
    
    def as_dict(self):
        return {tp:self.tp, tn:self.tn, fp:self.fp, fn:self.fn}
    
    def update(self, truth, prediction, filename=""):
        if truth!=self.pos_tag and truth!=self.neg_tag:
            raise ValueError("Invaid tag for truth.")
        if prediction!=self.pos_tag and prediction!=self.neg_tag:
            raise ValueError("Invaid tag for prediction.")
        # Negative/positive is inverted here
        # true means ham
        # false means spam
        truth = truth!=self.pos_tag
        prediction = prediction!=self.pos_tag
    
        if truth and prediction:
            self.tp+=1
        elif not truth and prediction:
            if filename!="":
                print("False positive: ", filename)
            self.fp+=1
        elif not truth:
            self.tn+=1
        else:
            if filename!="":
                print("False negative: ", filename)
            self.fn+=1
        
            
    def compute_from_dicts(self, truth_dict, pred_dict):
        for email, truth in truth_dict.items():
            prediction = None
            try:
                prediction=pred_dict[email]
            except KeyError:
                raise ValueError("Invalid prediction database.")
            self.update(truth, prediction, email)
    def quality_score(self):
        TP = self.tp
        TN = self.tn
        FP = self.fp
        FN = self.fn
        return (TP+TN)/(TP+TN+10*FP+FN)