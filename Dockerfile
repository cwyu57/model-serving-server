FROM python:latest
ADD . /app
RUN apt-get update
RUN apt-get install ffmpeg -y
RUN pip install torch torchvision fastapi
WORKDIR /app
EXPOSE 8000
CMD ["python", "app/main.py"]