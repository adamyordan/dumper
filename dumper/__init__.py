from flask import Flask, request, url_for
from flask_cors import CORS, cross_origin
from flask_httpauth import HTTPBasicAuth
import os
import time
import random, string

if not os.path.exists('data'):
    os.mkdir('data')

def _dump(data):
    filename = '{id}.{r}.txt'.format(id=time.strftime('%Y-%m-%d-%H%M%S'), r=_random_string(4))
    open(os.path.join('data', filename), 'w').write(data)

def _random_string(N):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(N))

def get_app():
    app = Flask(__name__)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    auth = HTTPBasicAuth()

    @auth.get_password
    def get_pw(username):
        if 'password' not in os.environ or not os.environ['password']:
            return ''
        else:
            return os.environ['password']

    @app.route('/dump/', methods=['GET', 'POST', 'OPTIONS'])
    @cross_origin()
    def endpoint_dump():
        if request.method == 'POST':
            d = request.get_data().decode()
        else:
            d = request.args.get('e')
        if d: _dump(d)
        return ''

    @app.route('/dump/result/')
    @auth.login_required
    def endpoint_results():
        results = []
        for _, _, files in os.walk('./data/'):
            for name in files:
                results.append(name)
        return '<br>\n'.join([ '<a href={r_url}> {r} </a>'.format(r_url=url_for('endpoint_file', r=r), r=r) for r in sorted(results) ])

    @app.route('/dump/result/<r>')
    @auth.login_required
    def endpoint_file(r):
        with open(os.path.join('.', 'data', os.path.basename(r)), 'r') as f:
            return f.read(), 200, {'Content-Type': 'text/plain'}
    
    return app

if __name__ == '__main__':
    get_app().run(host='0.0.0.0', debug=False)
