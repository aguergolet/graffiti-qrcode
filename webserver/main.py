import os
import sys
from flask import Flask, Blueprint, redirect, url_for, session, render_template, request
from tlgCode import tlgCode
import hashlib
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth

load_dotenv()

base_path=os.getenv('APPLICATION_ROOT', '/')
server_name = os.getenv('SERVER_NAME', '')
app = Flask(__name__, static_folder='./static', static_url_path=f'/content/',)
app.secret_key = os.urandom(24)
if server_name != '': 
    app.config['SERVER_NAME'] = os.getenv('SERVER_NAME', '127.0.0.1:5000')
    app.config['PREFERRED_URL_SCHEME'] = os.getenv('PREFERRED_URL_SCHEME', 'http')

bp = Blueprint('bp', __name__, url_prefix=f'{base_path}')
oauth = OAuth(app)


# Configure Google OAuth2
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'email'}
)

@bp.route(f'/pudim')
def pudim():
    return url_for('bp.authorize', _external=True, _scheme=app.config['PREFERRED_URL_SCHEME'])

@bp.route(f'/')
def index():
    user_alias =  get_user_alias()

    return render_template('index.html', user_logged_in=is_authenticated(), user_name=get_user_info(), error='', generated_files=get_user_files(f'./static/user/{user_alias}/'), folder=user_alias)

@bp.post(f'/gerar-qr-code')
def generate_qr():
    user_alias =  ""
    url = request.form['basic-url']
    error = ''
    if not url.startswith('http'):
        error = f'Sua URL deve iniciar com http.\nVocê informou {url}'
    else:
        user_alias = get_user_alias()
        print(user_alias)
        filename = generate_file_name(url)
       
        os.makedirs(f'./static/user/{user_alias}', exist_ok=True)
        # Exemplo de uso da classe
        generator = tlgCode.TLGCode()
        generator.generate_qr_code(url)
        qr_code_matrix = generator.get_qr_code_matrix()

        if qr_code_matrix is not None:

            qr_code_image = generator.generate_image()
            qr_code_image.save(f'./static/user/{user_alias}/{filename}.png')
            generator.generate_stl(f'./static/user/{user_alias}/{filename}')

    return render_template('index.html', user_logged_in=is_authenticated(), user_name=get_user_info(), error=error, generated_files=get_user_files(f'./static/user/{user_alias}/'), folder=user_alias)

@bp.route(f'/login')
def login():
    redirect_uri = url_for('bp.authorize', _external=True,  _scheme=app.config['PREFERRED_URL_SCHEME'])
    return google.authorize_redirect(redirect_uri)

@bp.route(f'/login/callback')
def authorize():
    token = google.authorize_access_token()
    if token is None:
        return 'Acesso negado.'
    session['google_token'] = (token['access_token'], '')
    userinfo = google.get('userinfo')
    session['user_email'] = userinfo.json().get('email')
    return redirect(url_for('bp.index'))

def is_authenticated():
    if 'user_email' in session:
        return True
    else:
        return False


def get_user_info():
    if is_authenticated():
        return session['user_email']
    else: 
        return ""

def get_user_files(directory):
    arquivos = []
    os.makedirs(directory, exist_ok=True)
    # Listar todos os arquivos no diretório
    todos_arquivos = os.listdir(directory)
    
    # Filtrar apenas os arquivos PNG
    arquivos_png = [f for f in todos_arquivos if f.endswith('.png')]

    for png in arquivos_png:
        nome_base = os.path.splitext(png)[0]
        stl = nome_base + '.stl'
        
        if stl in todos_arquivos:
            arquivos.append([png, stl])
        else:
            arquivos.append([png, ""])
    return arquivos

    

def get_user_alias():
    if is_authenticated():
        return str(hashlib.md5( session['user_email'].encode("utf-8")).hexdigest())
    else: 
        return ""

def generate_file_name(url):
    url = url.replace(':', '_')
    url = url.replace('/', '_')
    url = url.replace('.', '_')
    url = url.replace('?', '_')
    url = url.replace('&', '_')
    url = url.replace('=', '_')
    return url

if __name__ == '__main__':
    app.register_blueprint(bp)
    app.run(debug=True, host="0.0.0.0", port=5000)