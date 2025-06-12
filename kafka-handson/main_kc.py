from flask import Flask, jsonify
from kafka_consumer import KafkaMessageConsumer,DeliverySemantics

app = Flask(__name__)

kafka_consumer=KafkaMessageConsumer(
        bootstrap_servers="localhost:9092",
        group_id="reading_consumer1", # where this consumer group will get created?
        delivery_semantics=DeliverySemantics.AT_LEAST_ONCE
)

@app.route("/consume/<topic_name>",methods=["GET"])
def get_data(topic_name):
    try:
        message=kafka_consumer.start_consuming(topic_name)
        return jsonify({"messages": message}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__=="__main__":
    app.run(debug=True,port=5002)