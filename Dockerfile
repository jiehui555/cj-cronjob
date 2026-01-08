FROM docker.1ms.run/library/python:3.11-slim-bookworm

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt -i https://mirrors.ustc.edu.cn/pypi/simple

CMD ["python", "main.py"]
