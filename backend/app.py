from flask import Flask, request, jsonify
from newspaper import Article
import nltk
from flask_cors import CORS

nltk.download('punkt')

app = Flask(__name__)
CORS(app)  # Enable CORS for Chrome Extension

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "URL is missing."}), 400

    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        return jsonify({
            "title": article.title or "N/A",
            "author": ", ".join(article.authors) if article.authors else "N/A",
            "date": str(article.publish_date) if article.publish_date else "N/A",
            "summary": article.summary or "N/A"
        })
    except Exception as e:
        return jsonify({"error": f"Failed to summarize article: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000)
