FROM python:3.11-slim-bookworm AS builder
WORKDIR /app
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim-bookworm
WORKDIR /app
COPY --from=builder /venv /venv
ENV PYTHONUNBUFFERED=1
ENV PATH="/venv/bin:$PATH"
RUN playwright install --with-deps chromium \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY . .
CMD ["python", "main.py", "--schedule"]
