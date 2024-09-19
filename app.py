from flask import Flask, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import os
import requests

app = Flask(__name__)

GITHUB_REPO = "j1L860/7"
GITHUB_TOKEN = "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"  # Replace with your GitHub Token
GITHUB_USERNAME = "j1L860"

def preprocess_input_file(input_filepath, output_filepath):
    with open(input_filepath, 'r') as infile, open(output_filepath, 'w') as outfile:
        for line in infile:
            if line.startswith('#'):
                continue
            # Remove unwanted characters
            line = line.replace('/', '').replace('->', '').replace('"', '')
            line = line.replace('ALLELE', 'RESULT')
            outfile.write(line)

def upload_to_github(filepath, filename):
    with open(filepath, 'rb') as file:
        content = file.read()
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{filename}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/vnd.github.v3+json",
    }
    data = {
        "message": f"Add {filename}",
        "content": content.encode("base64"),  # For Python 3.8+, use base64.b64encode(content).decode()
    }
    response = requests.put(url, json=data, headers=headers)
    return response

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    raw_input_file = 'FileS.txt'
    file.save(raw_input_file)

    cleaned_input_file = 'updated_input.txt'
    preprocess_input_file(raw_input_file, cleaned_input_file)
    
    sample_data = pd.read_csv(cleaned_input_file)
    reference_data = pd.read_csv('j_hg38_ref.txt')

    # The rest of your processing code goes here...
    
    # Save plot to file
    plt.savefig('Haplogroup_Predict.png', dpi=300, bbox_inches='tight')

    # Upload results back to GitHub
    upload_response = upload_to_github(cleaned_input_file, 'updated_input.txt')
    plot_response = upload_to_github('Haplogroup_Predict.png', 'Haplogroup_Predict.png')

    return jsonify({
        "message": "File processed and results uploaded to GitHub",
        "updated_file_url": upload_response.json().get('content', {}).get('html_url', ''),
        "plot_url": plot_response.json().get('content', {}).get('html_url', ''),
    })

if __name__ == '__main__':
    app.run(debug=True)
