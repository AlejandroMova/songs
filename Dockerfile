FROM python:3.9

WORKDIR /songs

COPY main.py
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
