import uvicorn
from t0d0d0d0.backends.rest.app import app


if __name__ == "__main__":
    uvicorn.run(app, port=8011, host='0.0.0.0')