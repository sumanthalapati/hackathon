from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape_website():
    try:
        # Get the URL from the request JSON data
        data = request.get_json()
        url = data.get('url')

        # Set headers to mimic a real browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Send a GET request to the website with the headers
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the website content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the inner text of the <body> tag
            body_text = soup.body.get_text()

            # Clean up the text by removing extra white spaces and newlines
            cleaned_text = ' '.join(body_text.split())

            return jsonify({"cleaned_text": cleaned_text})

        else:
            return jsonify({"error": f"Failed to retrieve the website. Status code: {response.status_code}"})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
