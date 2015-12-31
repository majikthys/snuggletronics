import os.path
from flask import Flask
app = Flask(__name__)

import heated_mattress.views

resource_path = os.path.join(os.path.split(__file__)[0], "resources")

