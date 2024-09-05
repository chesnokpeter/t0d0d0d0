import uvicorn

from t0d0d0d0.restback.app import app

if __name__ == '__main__':
    uvicorn.run(app, port=8012, host='0.0.0.0')
