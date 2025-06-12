from kafka_producer import RateLimitedKafkaProducer
from flask import Flask,request,jsonify

app = Flask(__name__)

#TODO: write an efficient logger that captures the client-id as well.


bootstrap_servers="localhost:9092"
producer = RateLimitedKafkaProducer(bootstrap_servers=bootstrap_servers)

# design the 
@app.route('/push/<topic_name>',methods=["POST"])
def get_data(topic_name):
    # validate if the message is not in the correct form.
    try:
        message=request.get_json()
        print(message)
        if message and isinstance(message,dict):
            producer.send_message(message,topic=topic_name)
            return jsonify(message),201
        
        return jsonify({"error": "Invalid message format"}), 400 
    
    except Exception as e:
        print(f"exception occurred as {e}")
        return jsonify({"error": str(e)}), 500


# what are different ways we can send the data to a kafka topic.
# for _ in range(10):
#     data=generate_payment_data()
#     producer.send_message(data)
#     print("Data written to a kafka topic")

if __name__=="__main__":
    app.run(debug=True)
    

# how do i get the logs of the previous in the latest main
# discuss tradeoff for one producer per-topic or one producer all the topics

## ?: one flask server per single producer or i can have the multiple producers?
