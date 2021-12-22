from flask import Flask, render_template, request
import google.auth
from google.cloud import translate

app = Flask(__name__)
_, PROJECT_ID = google.auth.default()
TRANSLATE = translate.TranslationServiceClient()
PARENT = 'projects/{}'.format(PROJECT_ID)
SOURCE, TARGET = ('en', 'English'), ('es', 'Spanish')

# . . . [translate() function definition] . . .

if __name__ == '__main__':
    import os
    app.run(debug=True, threaded=True, host='0.0.0.0',
            port=int(os.environ.get('PORT', 8080)))

@app.route('/', methods=['GET', 'POST'])
def translate(gcf_request=None):
    """
    main handler - show form and possibly previous translation
    """

    # Flask Request object passed in for Cloud Functions
    # (use gcf_request for GCF but flask.request otherwise)
    local_request = gcf_request if gcf_request else request

    # reset all variables (GET)
    text = translated = None

    # if there is data to process (POST)
    if local_request.method == 'POST':
        text = local_request.form['text']
        data = {
            'contents': [text],
            'parent': PARENT,
            'target_language_code': TARGET[0],
        }
        # handle older call for backwards-compatibility
        try:
            rsp = TRANSLATE.translate_text(request=data)
        except TypeError:
            rsp = TRANSLATE.translate_text(**data)
        translated = rsp.translations[0].translated_text

    # create context & render template
    context = {
        'orig':  {'text': text, 'lc': SOURCE},
        'trans': {'text': translated, 'lc': TARGET},
    }
    return render_template('index.html', **context)
