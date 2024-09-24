from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Hugging Face API URL and Token
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}  # Replace with your actual Hugging Face token

# Route to serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle summarization
@app.route('/summarize', methods=['POST'])
def summarize():
    input_text = request.json.get('text')

    if input_text:
        payload = {"inputs": input_text}
        try:
            # Making the request to Hugging Face API
            response = requests.post(API_URL, headers=headers, json=payload)

            # Log the full response for debugging
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Content: {response.content}")
            
            if response.status_code == 200:
                result = response.json()
                summary = result[0].get('summary_text', 'No summary found in the response')
                return jsonify({'summary': summary})
            else:
                return jsonify({'summary': f"Error in summarization: {response.content.decode('utf-8')}"})
        except Exception as e:
            return jsonify({'summary': f"Error: {str(e)}"})
    else:
        return jsonify({'summary': "No text provided"})

if __name__ == '__main__':
    app.run(debug=True)
