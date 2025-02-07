from flask import Flask, request, jsonify
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

app = Flask(__name__)

# Initialize Presidio engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

@app.route('/anonymize', methods=['POST'])
def anonymize_text():
    data = request.json
    text = data.get("text", "")

    # Analyze the text for PII
    results = analyzer.analyze(text=text, entities=["PERSON", "PHONE_NUMBER"], language="en")

    # Anonymize detected PII
    anonymized_text = anonymizer.anonymize(text=text, analyzer_results=results)

    return jsonify({"original": text, "anonymized": anonymized_text.text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
