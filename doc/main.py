from difflib import SequenceMatcher
import os
from flask import current_app
import uuid

def check_plagiarism(request):
    if 'file1' not in request.files or 'file2' not in request.files:
        return {'error': 'No files provided'}

    file1 = request.files['file1']
    file2 = request.files['file2']

    # Save the uploaded files with unique names
    upload_dir = os.path.join(current_app.root_path, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    file1_path = os.path.join(upload_dir, f"{uuid.uuid4().hex}_{file1.filename}")
    file1.save(file1_path)
    file2_path = os.path.join(upload_dir, f"{uuid.uuid4().hex}_{file2.filename}")
    file2.save(file2_path)

    # Read the contents of the files
    try:
        with open(file1_path, 'rb') as f1, open(file2_path, 'rb') as f2:
            file1_content = f1.read().decode('utf-8', errors='replace')
            file2_content = f2.read().decode('utf-8', errors='replace')
    except Exception as e:
        os.remove(file1_path)
        os.remove(file2_path)
        return {'error': 'Unable to check for plagiarism. Please try again.'}

    # Compare the files using SequenceMatcher
    try:
        similarity_ratio = SequenceMatcher(None, file1_content, file2_content).ratio()
        plagiarism_percentage = int(similarity_ratio * 100)
    except Exception as e:
        os.remove(file1_path)
        os.remove(file2_path)
        return {'error': 'Unable to check for plagiarism. Please try again.'}

    # Remove the uploaded files
    os.remove(file1_path)
    os.remove(file2_path)

    return {'plagiarism_percentage': plagiarism_percentage}
