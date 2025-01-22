from flask import Blueprint, render_template, request
import warnings
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet, stopwords
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

warnings.filterwarnings("ignore", category=DeprecationWarning)

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name().replace("_", " ").replace("-", " ").lower()
            synonym = "".join([char for char in synonym if char.isalnum()])
            synonyms.append(synonym)
    return synonyms

def semantic_similarity(word1, word2):
    word1_synonyms = set(get_synonyms(word1))
    word2_synonyms = set(get_synonyms(word2))
    if not word1_synonyms or not word2_synonyms:
        return 0
    similarity = len(word1_synonyms.intersection(word2_synonyms)) / (len(word1_synonyms.union(word2_synonyms)) or 1)
    return similarity

def paraphrase_sentence(sentence):
    words = word_tokenize(sentence)
    paraphrased_words = []
    for word in words:
        if word.lower() not in stop_words:  
            synonyms = get_synonyms(word)
            if synonyms:
                synonyms.sort(key=lambda x: semantic_similarity(x, word), reverse=True)
                paraphrased_words.append(synonyms[0])
            else:
                paraphrased_words.append(word)
        else:
            paraphrased_words.append(word)
    return ' '.join(paraphrased_words)

def rephrase_paragraph(text):
    sentences = sent_tokenize(text)
    return ' '.join([paraphrase_sentence(sentence) for sentence in sentences])

def summarize_paragraph_text_rank(paragraph, num_sentences=3):
    try:
        summarizer = TextRankSummarizer()
        parser = PlaintextParser.from_string(paragraph, Tokenizer("english"))
        summary = summarizer(parser.document, num_sentences)
        return "\n".join(str(sentence) for sentence in summary)
    except Exception as e:
        return f"Error occurred during summarization: {str(e)}"

def generate_points(paragraph):
    words = word_tokenize(paragraph)
    words = [word for word in words if word.lower() not in stop_words]  
    fdist = nltk.FreqDist(words)
    keyword_list = [word for word, _ in fdist.most_common(5)]
    points = []
    sentences = sent_tokenize(paragraph)
    for i, sentence in enumerate(sentences, start=1):
        words = word_tokenize(sentence)
        common_keywords = set(words) & set(keyword_list)
        if common_keywords:
            paraphrased_sentence = paraphrase_sentence(sentence)
            points.append(f"{i}. {paraphrased_sentence}")  
    return points

app_paraphrase = Blueprint('app_paraphrase', __name__, template_folder='templates')

@app_paraphrase.route('/', methods=['GET', 'POST'])
def paraphrase():
    if request.method == 'POST':
        input_text = request.form['input_text']
        option = request.form['option']

        if option == 'rephrase':
            output_text = rephrase_paragraph(input_text)
        elif option == 'summarize':
            output_text = summarize_paragraph_text_rank(input_text)
        elif option == 'points':
            output_text = "\n".join(generate_points(input_text))
        else:
            output_text = "Invalid option selected."
    else:
        output_text = ""

    return render_template('paraphrase.html', output_text=output_text)
