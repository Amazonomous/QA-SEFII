from app import create_app
import pytest

app = create_app()

if __name__ == '__main__':
    pytest.main() # Run tests before launch
    app.run(host="0.0.0.0", port=10000, debug=True, use_reloader=False)