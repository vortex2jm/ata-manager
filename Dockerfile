FROM python:3.10

WORKDIR /ata-manager

COPY . .

RUN ln -sf /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime

RUN pip install -r documentation/requirements.txt

CMD ["python", "./src/main.py"] 