FROM python:3.9-slim
WORKDIR /main
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY alembic.ini .
COPY alembic/ ./alembic
COPY app/ ./app
CMD alembic upgrade head && uvicorn app.main:app --host=0.0.0.0