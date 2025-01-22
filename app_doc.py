from flask import Blueprint, render_template, request, jsonify
from doc.main import check_plagiarism

app_doc = Blueprint('app_doc', __name__, template_folder='templates')

@app_doc.route('/', methods=['GET', 'POST'])
def check_plagiarism_route():
    if request.method == 'POST':
        result = check_plagiarism(request)
        return jsonify(result)
    return render_template('doc.html')
