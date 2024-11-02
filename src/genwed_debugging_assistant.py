from flask import Flask, render_template, request, jsonify
from transformers import pipeline

genwed = pipeline("text-generation", model="./genwed")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_suggestion", methods=["POST"])
def get_suggestion():
    data = request.json
    user_prompt = data.get("prompt")

    response = genwed(user_prompt, max_length=200, num_return_sequences=1)
    suggestion = response[0]["generated_text"]
    
    refined_suggestion = "Here’s a suggestion:\n" + suggestion.strip()
    
    return jsonify({"suggestion": refined_suggestion})

if __name__ == "__main__":
    app.run(debug=True)
