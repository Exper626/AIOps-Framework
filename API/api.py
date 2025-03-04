from flask import Flask, request, jsonify
import ollama


app = Flask(__name__)


@app.route('/', methods=["POST"])
def requestLLM():

    if not data:
        return jsonify({"error":"No json data"}),400

    data = request.get_json()

    model = data.get('model')
    source = data.get('source')
    sentence_transformer = data.get('sentence_transformer') 

    text = LLMProcessor(model, source, sentence_transformer)

    return jsonify({"message":text})



def LLMProcessor():
    
    






if __name__ == "main"
    app.run(host="0.0.0.0", port=9091)
