from flask import Flask, render_template , send_from_directory 
from app_doc import app_doc
from app_perplexity import app_perplexity
from app_paraphrase import app_paraphrase

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Register blueprints
app.register_blueprint(app_perplexity, url_prefix='/perplexity')
app.register_blueprint(app_doc, url_prefix='/doc')
app.register_blueprint(app_paraphrase, url_prefix='/paraphrase')

@app.route('/contact')
def contact():
    return render_template('contact/index.html')

@app.route('/about')
def about():
    return render_template('about/index.html')



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


