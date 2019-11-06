from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'

csrf = CSRFProtect(app)

from currency_changer import routes
