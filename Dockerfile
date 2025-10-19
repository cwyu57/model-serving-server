FROM python:latest

RUN apt-get update
RUN apt-get install ffmpeg -y
RUN pip install torch torchvision fastapi uvicorn
WORKDIR /app
ADD . .

EXPOSE 8000

CMD ["python", "app/main.py"]
