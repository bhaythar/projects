import os

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    """Return a friendly http"""
    message="ITS RUNNING"

    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render_template('index.html',
    message=message
    service=service
    Revision=revision)


if __name__ =="__main__";
    app.run(debug=True,host='0.0.0.0' ,port=int(os.environ.get('PORT', 8080)))
