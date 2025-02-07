import sys

import numpy as np
import pandas as pd
import pythainlp

class TextClassifier:

    def __init__(self, csv_file_name):
        self.model_params = pd.read_csv(csv_file_name, index_col=0)

    def compute_probability(self, thai_text_string):
        tokenized_texts = pythainlp.tokenize.word_tokenize(thai_text_string)
        labels = self.get_all_possible_labels()
        
        scores = {label: 0.0 for label in labels}
        
        for tokenized_text in tokenized_texts:
            if tokenized_text in self.model_params.index:
                for label in labels:
                    scores[label] += self.model_params.loc[tokenized_text, label]
        
        label_exp_values = {}
        
        for each_label in scores:
            label_exp_values[each_label] = np.exp(scores[each_label])
            
        sum_exp = 0.0
        
        for value in label_exp_values.values():
            sum_exp += value
        
        prob = {}
        
        for each_label in label_exp_values:
            prob[each_label] = label_exp_values[each_label] / sum_exp
        
        final_prob = {}
        
        for key, value in prob.items():
            final_prob[key] = value
        
        return final_prob

    def get_all_possible_features(self):
        return list(self.model_params.index)

    def get_all_possible_labels(self):
        return list(self.model_params.columns)

    def classify(self, thai_text_string):
        final_prob = self.compute_probability(thai_text_string)
        return max(final_prob, key=final_prob.get)


    # if __name__ == '__main__':
    #     if (len(sys.argv) != 2):
    #         print('usage:\tpython logistic_regression.py <model_file>')
    #         sys.exit(0)
    #     model_file_name = sys.argv[1]
    #     model = TextClassifier(model_file_name)


# csv_file_name = "toy_model.csv"

# text = "ฉันเกลียดฝุ่น"
# model = TextClassifier(csv_file_name)
# print(model.get_all_possible_features())
# print(model.get_all_possible_labels())
# print(model.compute_probability(text))
# print(model.classify(text))