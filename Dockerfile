FROM python:3.12-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
CMD ["python", "-u", "./main.py"]
