from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# root directory
@app.route('/')
def index():
    return render_template('index.html')
    
# watch news
@app.route('/news', methods=['POST'])
def news():
    level = request.form.get('cefr')
    count = int(request.form.get('count'))
    news_type = request.form.get('news_type')

    # suppose is txt file
    news_path = f"data/news/{news_type}.txt"

    with open(news_path, 'r', encoding='utf-8') as f:
        news_content = f.read()

    return render_template(
        'news.html',
        news=news_content,
        level=level,
        count=count,
        news_type=news_type
    )


@app.route('/learn', methods=['POST'])
def learn():
    level = request.form.get('cefr')
    count = int(request.form.get('count'))

    # the file received
    json_path = os.path.join('data/vocabulary', 'words.json')

    with open(json_path, 'r', encoding='utf-8') as f:
        words = json.load(f)

    # choose the number of voc 
    selected = words[:count]

    return render_template(
        'vocabulary.html', 
        words = selected,
        level = level,
        feedback = {}
    )




# use vocabulary make sentence
@app.route('/check_sentence', methods=['POST'])
def check_sentence():
    word = request.form.get('word')
    sentence = request.form.get('sentence')
    level = request.form.get('level')
    count = int(request.form.get('count'))

    # mock reply
    mock_result = {
        "word": word,
        "user_sentence": sentence,
        "is_correct": False if "bad" in sentence else True,
        "explanation": "Example, false if bad inside"
    }

    # load vocabulary
    json_path = os.path.join('data/vocabulary', 'words.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        all_words = json.load(f)

    words = all_words[:count]

    # not redirect, add anchor
    return render_template(
        'vocabulary.html',
        words=words,
        level=level,
        feedback={word: mock_result},
        anchor=word   # use for scroll 
    )
















if __name__ == '__main__':
    app.run(debug=True)
