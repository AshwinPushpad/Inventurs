from flask import Flask, request, jsonify

from dotenv import load_dotenv
import os

from google import genai


app = Flask(__name__)


load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def generate_text(prompt):
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    print(f"Generated response: {response}")
    return response.candidates[0].content.parts[0].text.strip()

def log_to_file(prompt, response):
    with open("logs.txt", "a") as log_file:
        log_file.write(f"Prompt: {prompt}\nResponse: {response}\n\n")

@app.route('/')
def index():
    return "Welcome to the Flask API APP!"

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing "prompt" in JSON payload'}), 400
        
        prompt = data['prompt']
        response_text = generate_text(prompt)
        if not response_text:
            return jsonify({'error': 'No response generated'}), 500
        
        log_to_file(prompt, response_text)

        return jsonify({'response': response_text})

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    app.run(debug=True)
