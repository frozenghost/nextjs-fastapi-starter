FROM python:3.10-alpine AS backend-step1

WORKDIR /workspace

COPY requirements.txt ./

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

WORKDIR /workspace

CMD alembic upgrade head && uvicorn api.index:app --host 0.0.0.0 --port 8000

# ["alembic", "upgrade", "head", ";", "uvicorn", "api.index:app", "--host", "0.0.0.0", "--port", "8000"]