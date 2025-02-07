import pandas as pd
import numpy as np
from pythainlp.tokenize import word_tokenize  # ใช้ตัดคำภาษาไทย

class TextClassifier:
    def __init__(self, csv_file):
        """ โหลดค่าพารามิเตอร์จากไฟล์ CSV """
        self.model_parameters = pd.read_csv(csv_file)  # โหลดข้อมูล
        self.model_parameters.set_index("word", inplace=True)  # ตั้งค่าคอลัมน์แรกเป็น index

    def get_all_possible_features(self):
        """ คืนค่ารายการคำทั้งหมดที่เป็น feature ของโมเดล """
        return list(self.model_parameters.index)

    def get_all_possible_labels(self):
        """ คืนค่ารายการ label ทั้งหมดที่โมเดลสามารถทำนายได้ """
        return list(self.model_parameters.columns)

    def compute_probability(self, text):
        """ คำนวณค่าความน่าจะเป็นของแต่ละ label """
        tokens = word_tokenize(text)  # ตัดคำภาษาไทย
        labels = self.get_all_possible_labels()

        scores = {label: 0.0 for label in labels}  # เริ่มต้นคะแนนเป็น 0

        for token in tokens:
            if token in self.model_parameters.index:
                for label in labels:
                    scores[label] += self.model_parameters.loc[token, label]

        # ใช้ softmax function แปลงคะแนนเป็นค่าความน่าจะเป็น
        exp_scores = {label: np.exp(score) for label, score in scores.items()}
        sum_exp = sum(exp_scores.values())

        probabilities = {label: exp_score / sum_exp for label, exp_score in exp_scores.items()}
        return probabilities

    def classify(self, text):
        """ ทำนาย label ที่มีค่าความน่าจะเป็นสูงสุด """
        probabilities = self.compute_probability(text)
        return max(probabilities, key=probabilities.get)


# โหลดโมเดลจาก toy_model.csv
model = TextClassifier("toy_model.csv")

# ทดสอบพยากรณ์ข้อความ
text_sample = "ฉันเกลียดฝุ่น"
prediction = model.classify(text_sample)
probabilities = model.compute_probability(text_sample)

print(f"ข้อความที่ป้อนเข้า: {text_sample}")
print(f"Label ที่คาดการณ์ได้: {prediction}")
print(f"ค่าความน่าจะเป็น: {probabilities}")

print(model.get_all_possible_features)