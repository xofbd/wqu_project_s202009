from flask import Flask, render_template

from message import greet

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html', message=greet())


if __name__ == '__main__':
    app.run(debug=True)