from flask import Flask, jsonify, request, redirect, session, url_for
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = 'super-secret-key'  # Сменете с реален ключ за продукция

# Конфигурация на базата данни
# Променете с вашите настройки за връзка
app.config['DATABASE_URI'] = 'postgresql://user:password@localhost:5432/database'

# OAuth конфигурация
oauth = OAuth(app)
openid = oauth.remote_app(
    'openid',
    consumer_key='OPENID_CLIENT_ID',  # Сменете с вашето client_id от OpenID провайдера
    consumer_secret='OPENID_CLIENT_SECRET',  # Сменете с вашия client_secret
    request_token_params={'scope': 'email'},
    base_url='https://<openid-provider-url>/api',  # URL на вашето OpenID API
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://<openid-provider-url>/token',
    authorize_url='https://<openid-provider-url>/auth'
)

@app.route('/')
def index():
    if 'openid_token' in session:
        return jsonify(message="Ти си аутентикиран"), 200
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return openid.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('openid_token', None)
    return jsonify(message="Излязохте успешно"), 200

@app.route('/login/authorized')
def authorized():
    resp = openid.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return jsonify(message="Достъпът е отказан"), 403

    session['openid_token'] = (resp['access_token'], '')
    return jsonify(message="Успешна аутентикация"), 200

@openid.tokengetter
def get_openid_oauth_token():
    return session.get('openid_token')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3000)

