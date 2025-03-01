import uvicorn

from t0d0d0d0.http.app import create_app

if __name__ == "__main__":
    uvicorn.run(
        create_app,
        factory=True,
        port=8011
    )