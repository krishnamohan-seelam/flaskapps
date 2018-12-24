import os
from flask import Flask

config_name = 'development'
app = Flask(__name__)
cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
app.config.from_pyfile(cfg)

from . import routes