import os
import sys
from flask import Flask, Blueprint, redirect, url_for, session, render_template, request
from werkzeug.utils import secure_filename
import re
from urllib.parse import urlparse # Added import
from tlgCode import tlgCode
import hashlib
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth

load_dotenv()

base_path=os.getenv('APPLICATION_ROOT', '/')
server_name = os.getenv('SERVER_NAME', '')
app = Flask(__name__, static_folder='./static', static_url_path=f'{base_path}/content/',)

# Improved secret key management
secret_key_env = os.getenv('SECRET_KEY')
is_development_env = os.getenv('FLASK_ENV') == 'development'

if not secret_key_env:
    if is_development_env:
        print("INFO: SECRET_KEY environment variable not set. Using a dynamically generated key for development.", file=sys.stderr)
        app.secret_key = os.urandom(24)
    else:
        print("CRITICAL WARNING: SECRET_KEY environment variable not set. Using a temporary, insecure key. "
              "THIS IS NOT SUITABLE FOR PRODUCTION. SET A STRONG SECRET_KEY ENVIRONMENT VARIABLE.", file=sys.stderr)
        app.secret_key = os.urandom(24) # Fallback, but insecure for prod
else:
    app.secret_key = secret_key_env

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
    user_alias =  "" # Initialize user_alias, it will be set later if needed
    url = request.form['basic-url']
    error = ''
    
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme in ['http', 'https']:
            error = f"URL inválida: O esquema deve ser 'http' ou 'https'. Você informou '{url}'"
        elif not parsed_url.netloc:
            error = f"URL inválida: Não foi possível identificar um domínio na URL. Você informou '{url}'"
    except ValueError: # urlparse can raise ValueError for malformed URLs, though it often tries its best
        error = f"URL mal formada: A URL fornecida não pôde ser processada. Você informou '{url}'"

    if error:
        # If there's an error, get user_alias for rendering the template correctly
        user_alias = get_user_alias() 
        # Note: generated_files might be empty or from a previous successful attempt if user_alias exists
        # It's generally okay to show previous files even if current input has an error
        generated_files_list = get_user_files(f'./static/user/{user_alias}/') if user_alias else []
        return render_template('index.html', user_logged_in=is_authenticated(), user_name=get_user_info(), error=error, generated_files=generated_files_list, folder=user_alias)
    else:
        # No validation error, proceed with QR code generation
        user_alias = get_user_alias()
        # Ensure user_alias is available; if not (e.g., not logged in, though UI should prevent this flow), set a default or handle error
        if not user_alias:
             # This case should ideally be handled by authentication checks earlier
             # For now, setting a generic error if user_alias is somehow empty post-validation
            error = "Erro de autenticação ou sessão. Por favor, tente logar novamente."
            # Attempt to get user_alias again just in case, or set to a placeholder if truly anonymous is possible and desired
            # However, the structure implies user_alias is tied to being logged in.
            # Showing an error is safer.
            return render_template('index.html', user_logged_in=is_authenticated(), user_name=get_user_info(), error=error, generated_files=[], folder="")

        print(user_alias) # For debugging
        filename = generate_file_name(url)
       
        os.makedirs(f'./static/user/{user_alias}', exist_ok=True)
        generator = tlgCode.TLGCode()
        generator.generate_qr_code(url)
        qr_code_matrix = generator.get_qr_code_matrix()

        if qr_code_matrix is not None:
            qr_code_image = generator.generate_image()
            qr_code_image.save(f'./static/user/{user_alias}/{filename}.png')
            generator.generate_stl(f'./static/user/{user_alias}/{filename}')
        
        # After successful generation, render template with updated files
        return render_template('index.html', user_logged_in=is_authenticated(), user_name=get_user_info(), error='', generated_files=get_user_files(f'./static/user/{user_alias}/'), folder=user_alias)

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
    # Use secure_filename to handle common path traversal and sanitization
    filename = secure_filename(url)
    # Replace potentially problematic characters that secure_filename might allow
    # This example allows alphanumeric, underscore, and a single dot for extensions.
    filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    # Prevent names that are just dots or start with dots.
    if not filename or filename.startswith('.'):
        # Prepend with an underscore if it's empty, just dots, or starts with a dot.
        filename = "_" + filename 
    # Ensure the filename is not overly long and does not consist only of underscores
    if not filename.strip('_'):
        filename = "default_filename" # Provide a default if it becomes empty after stripping underscores
    return filename[:200] # Limit filename length as an additional precaution

if __name__ == '__main__':
    app.register_blueprint(bp)
    # Set debug mode based on FLASK_ENV environment variable
    # Default to False (production mode) if FLASK_ENV is not 'development'
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)