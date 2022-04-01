# temp stage
FROM --platform=$BUILDPLATFORM python:3.9-bullseye as builder


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -f && \
    apt-get install -y gcc

RUN rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip install virtualenv

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /lorita-bot/backend


COPY ./backend/requirements.txt .
RUN pip install -r requirements.txt


# final stage
FROM python:3.9-slim

LABEL org.opencontainers.image.source="https://github.com/olidroide/lorita-bot/"
LABEL org.opencontainers.image.description="IMPROVEMENTS"

RUN addgroup --system app && adduser --system --group app
USER app

WORKDIR /lorita-bot/backend

COPY --from=builder /opt/venv /opt/venv
COPY ./backend/src /lorita-bot/backend/src
ENV PATH="/opt/venv/bin:$PATH"


#CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app:app"]
#CMD ["uvicorn", "src.app:app", "--workers", "3", "--limit-max-requests", "100000", "--host", "0.0.0.0"]
CMD ["python", "/lorita-bot/backend/src/main.py"]