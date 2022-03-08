from flask_app.models.model_connection import SplTokenViewerApiClient as Client 

from flask import Flask
app = Flask(__name__)
app.secret_key = "12321312653112"