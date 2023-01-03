from flask import Flask

app = Flask(__name__)

import serverlabs.views
import serverlabs.bl
import serverlabs.db