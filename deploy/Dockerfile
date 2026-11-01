FROM node:24-alpine AS frontend
RUN npm install -g pnpm@12.14.0
WORKDIR /src
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY frontend/package.json frontend/package.json
COPY packages/ui/package.json packages/ui/package.json
RUN pnpm install --frozen-lockfile
COPY frontend frontend
COPY packages/ui packages/ui
RUN pnpm --filter web build

FROM python:3.13-slim AS python-build
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /build
COPY requirements.lock .
RUN pip install --no-cache-dir --prefix=/install -r requirements.lock

FROM python:3.13-slim
COPY --from=python-build /install /usr/local
WORKDIR /app
COPY backend/app /app/app
COPY --from=frontend /src/frontend/dist /app/static
ENV PYTHONPATH=/app PYTHONUNBUFFERED=1 MCWEB_DB=/data/mcweb.sqlite3 MCWEB_STATIC_DIR=/app/static
USER 1000:1000
CMD ["python", "-m", "app.server"]
