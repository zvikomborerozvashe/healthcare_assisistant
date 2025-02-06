from app import create_app
from flask_cors import CORS

app = create_app()
CORS(app)  # Enable CORS for frontend requests

if __name__ == "__main__":
    app.run(debug=True)
