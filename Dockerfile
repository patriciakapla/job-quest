FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:0.11.19 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev 

COPY . .

EXPOSE 8000

CMD ["uv", "run", "fastapi", "dev", "job_quest/main.py", "--host", "0.0.0.0"]