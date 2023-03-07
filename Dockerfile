FROM python:3.7-slim
WORKDIR /main
# .env to be removed before deploy
# COPY .env .
COPY alembic.ini .
COPY alembic/ ./alembic
COPY app/ ./app
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
# ENV DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
CMD alembic upgrade head && uvicorn app.main:app --host=0.0.0.0