
from flask import Blueprint, render_template, request
from perplexity.main import check_plagiarism as perplexity_check_plagiarism

app_perplexity = Blueprint('app_perplexity', __name__, template_folder='templates')

@app_perplexity.route('/', methods=['GET', 'POST'])
def perplexity_plagiarism():
    if request.method == 'POST':
        text = request.form['text']
        result = perplexity_check_plagiarism(text)
        return render_template('perplexity_result.html', **result)
    return render_template('perplexity.html')
