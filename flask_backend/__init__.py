
from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)

cors = CORS(app)

from flask_backend import routes
