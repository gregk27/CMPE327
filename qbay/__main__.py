# Supress Flake8 warnings on the imports, as they are required but unused
from qbay import app
from qbay.models import * # NOQA
from qbay.backend import * # NOQA
from qbay.controllers import * # NOQA

"""
This file runs the server at a given port
"""
FLASK_PORT = 8081

if __name__ == "__main__":
    app.run(debug=True, port=FLASK_PORT, host='0.0.0.0')
