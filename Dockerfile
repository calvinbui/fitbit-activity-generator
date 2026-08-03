FROM python:3.14-bookworm

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
CMD ["python", "-u", "./main.py"]
