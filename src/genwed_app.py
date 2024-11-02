from flask import Flask, render_template, request, jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

try:
    tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
    model = AutoModelForCausalLM.from_pretrained("distilgpt2")
    
    genwed = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=-1 
    )
    
except Exception as e:
    print(f"Error loading model: {str(e)}")
    raise

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_suggestion", methods=["POST"])
def get_suggestion():
    data = request.json
    user_prompt = data.get("prompt")

    try:
        response = genwed(user_prompt, max_length=200, num_return_sequences=1)
        suggestion = response[0]["generated_text"]
        return jsonify({"suggestion": suggestion})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
