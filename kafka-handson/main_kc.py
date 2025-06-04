from flask import Flask, request,jsonify
from kafka_consumer import KafkaMessageConsumer

app = Flask(__name__)

kafka_consumer=KafkaMessageConsumer()

@app.route("/consume/<topic_name>",methods=["POST"])
def get_data(topic_name):
    kafka_consumer



if __name__=="__main__":
    app.debug(True)