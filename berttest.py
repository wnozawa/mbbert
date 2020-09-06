# load model
# import sentence_transformers
from sentence_transformers import SentenceTransformer
# from ..sentencetransformers.sentence_transformers
# あとでパス直す
import numpy as np

model_path = "training_bert_japanese"
model = SentenceTransformer(model_path)

import pandas
df_header = pandas.read_csv('AllQA.csv')
dg = df_header.iloc[:,0]


questions = dg.astype(str).tolist() # 文字列のリストに変換
# plain = '\n'.join(dglst)         # 空白文字で結合

# print(plain)
question_vectors = model.encode(questions)

import pickle
question_vectors_pickle_name="question_vectors.pickle"
f = open(question_vectors_pickle_name,'wb')
pickle.dump(question_vectors,f)
f.close

import pprint

# pprint.pprint(question_vectors)

# input を取って
# print('質問をどうぞ')
query = ['赤字でも売れますか？']
# input to vector by sentenceBERT
query_vector = model.encode(query)
# get similarities

# get best 10 questions
# pprint.pprint(query_vector)

import scipy

distances = scipy.spatial.distance.cdist(query_vector, question_vectors, metric="cosine")[0]

results = zip(range(len(distances)), distances)
results = sorted(results, key=lambda x: x[1])

print("\n\n======================\n\n")
print("Query:", query)
print("\nTop 5 most similar sentences in corpus:")

closest_n = 5

for idx, distance in results[0:closest_n]:
    print(questions[idx].strip(), "(Score: %.4f)" % (distance / 2))
