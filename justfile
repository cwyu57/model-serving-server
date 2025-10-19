build-dev:
    docker build -t model-serving-server .

dev:
    docker run -p 8000:8000 model-serving-server
