FROM mcr.microsoft.com/playwright/python:v1.64.0-resolute

ENV UV_LINK_MODE=copy \
    UV_PYTHON_INSTALL_DIR=/opt/uv-python \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev

CMD ["uv", "run", "--no-sync", "pytest"]
