from sentence_transformers import SentenceTransformer

# load BERT model
model_path = "training_bert_japanese"
model = SentenceTransformer(model_path)

# load Q&A
import pandas
df_header = pandas.read_csv('AllQA.csv')
dg = df_header.iloc[:,0]


questions = dg.astype(str).tolist() # 文字列のリストに変換

# vectorize questions
question_vectors = model.encode(questions)

# save question vectors
import pickle
question_vectors_pickle_name="question_vectors.pickle"
f = open(question_vectors_pickle_name,'wb')
pickle.dump(question_vectors,f)
f.close


# test BERT

query = ['赤字でも売れますか？']
# vectorize query by sentenceBERT
query_vector = model.encode(query)


import scipy

# compute similarity
distances = scipy.spatial.distance.cdist(query_vector, question_vectors, metric="cosine")[0]

results = zip(range(len(distances)), distances)
results = sorted(results, key=lambda x: x[1])

print("\n\n======================\n\n")
print("Query:", query)
print("\nTop 5 most similar sentences in corpus:")

# display closest 5 question to query
closest_n = 5

for idx, distance in results[0:closest_n]:
    print(questions[idx].strip(), "(Score: %.4f)" % (distance / 2))
