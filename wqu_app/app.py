import os
import vega


from flask import Flask, request, render_template

from message import greet, retrieve_local_ip_adress

app = Flask(__name__)
DEPLOY = os.getenv('DEPLOY')


@app.route('/')
def main():
    if DEPLOY == 'heroku':
        ip_address = request.headers['X-Forwarded-For']
    else:
        ip_address = retrieve_local_ip_adress()

    return render_template('index.html', message=greet(ip_address)[0], graph = greet(ip_address)[1])


if __name__ == '__main__':
    app.run(debug=True)
