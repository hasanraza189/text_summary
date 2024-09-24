from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Hugging Face API URL and Token
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "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"}  # Get token from Hugging Face

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/summarize', methods=['POST'])
def summarize():
    input_text = request.json.get('text')

    if input_text:
        payload = {"inputs": input_text}
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            # Log the full response for debugging
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Content: {response.content}")
            
            if response.status_code == 200:
                result = response.json()
                summary = result[0].get('summary_text', 'No summary found in the response')
                return jsonify({'summary': summary})
            else:
                return jsonify({'summary': f"Error in summarization: {response.content}"})
        except Exception as e:
            return jsonify({'summary': f"Error: {str(e)}"})
    else:
        return jsonify({'summary': "No text provided"})

if __name__ == '__main__':
    app.run(debug=True)
