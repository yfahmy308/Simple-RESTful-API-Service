import sys
import os

# Ensure the module is in the path for proper imports
sys.path.append(os.path.dirname(__file__))

from test2.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
