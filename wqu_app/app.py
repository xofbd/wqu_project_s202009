import os



from flask import Flask, request, render_template

from wqu_app.message import greet, retrieve_local_ip_adress

app = Flask(__name__)
DEPLOY = os.getenv('DEPLOY')


@app.route('/')
def main():
    if DEPLOY == 'heroku':
        ip_address=request.headers['X-Forwarded-For']
    else:
        ip_address=retrieve_local_ip_adress()
    results = dict(zip(('message', 'graph'), greet(ip_address)))
    return render_template('index.html', message=results['message'], graph=results['graph'])


if __name__ == '__main__':
    app.run(debug=True)
