# README
## ファイルの説明
- **AllQA.csv**  
  Q&Aのリスト。１列目にQ、２列目にA。
- **runtime.txt**
  herokuで利用するPythonのバージョンを指定するファイル。
- **sentence_transformers**  
  文章をベクトル化するモジュール。
- **main.py**  
- **Procfile**  
  heroku上の実行方法を指定するファイル。
- **question_vectors.pickle**  
  BERTでベクトルに変換されたQのリスト。
- **training_bert_japanese**  
  BERTの事前学習データのディレクトリ。
- **berttest.py**  
  BERTの動作確認のためのファイル。
- **requirements.txt**  
  herokuで利用するPythonモジュールを指定するファイル。

## 使い方
このリポジトリをクローンしたディレクトリでBERTの事前学習データをダウンロード（下を実行）。

    wget -O sonobe-datasets-sentence-transformers-model.tar "https://www.floydhub.com/api/v1/resources/JLTtbaaK5dprnxoJtUbBbi?content=true&download=true&rename=sonobe-datasets-sentence-transformers-model-2"
	tar -xvf sonobe-datasets-sentence-transf

BERTが動作するかを確認。

	python berttest.py

 正常に動作する場合は下が出力される。

	======================
	　
	Query: ['赤字でも売れますか？']

	Top 5 most similar sentences in corpus:
	赤字会社でも売れるのでしょうか？ (Score: 0.0339)
	赤字だが、売れるだろうか？ (Score: 0.0349)
	こんな小さな会社でも売れるのか。 (Score: 0.1029)
	売上等の企業規模は、どれくらいから対応してもらえますか?小さい会社でも売れますか? (Score: 0.1579)
	赤字であっても譲渡できるのですか？ (Score: 0.1594)
