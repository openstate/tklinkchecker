FROM python:3

WORKDIR /opt/tklinkchecker

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["tail", "-f", "requirements.txt"]
