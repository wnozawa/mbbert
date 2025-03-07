from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import datetime

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
DATABASE_URL = os.environ['DATABASE_URL']

import psycopg2

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'



# load model
from sentence_transformers import SentenceTransformer

model_path = "training_bert_japanese"
model = SentenceTransformer(model_path)

# load original Q&A
import pandas
QA = pandas.read_csv('AllQA.csv')


# load question_vectors
import pickle
question_vectors_pickle_name="question_vectors.pickle"
f = open(question_vectors_pickle_name,"rb")
question_vectors = pickle.load(f)
f.close()



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # response=LSI_prediction(event.message.text, dictionary, tfidf, lsi_model, index, text_corpus)
    query = [event.message.text]
    query_vector = model.encode(query)
    distances = scipy.spatial.distance.cdist(query_vector, question_vectors, metric="cosine")[0]
    sims_argmax = numpy.argmax(distances)
    # sims_argmax=TFIDF_sims_argmax(event.message.text, dictionary, tfidf, index, text_corpus)
    response=QA.iloc[sims_argmax,1]

    # conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    # cur = conn.cursor()
    # # cur.execute("create table demo(id int,data text)")
    #
    # dt_now = datetime.datetime.now()
    # cur.execute('insert into messagelog values(%s,%s,%s)', (event.message.text, response, dt_now.isoformat()))
    # conn.commit()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
