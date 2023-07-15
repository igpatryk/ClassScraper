FROM python:3.9.17-slim-bullseye

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN touch output.txt

CMD ["python","-u","main.py"]