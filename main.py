from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from prometheus_client import Counter, Histogram, Gauge, make_asgi_app
import models
import uvicorn
from routes import router
import time
import logging_loki
from multiprocessing import Queue
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor  # Re-add this import
import logging
import sys
import os
from telemetry_config import setup_telemetry_and_logging

setup_telemetry_and_logging()


# Database setup
models.Base.metadata.create_all(bind=engine)

# Prometheus core metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', [
                        'method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency',
                            ['method', 'endpoint', 'http_status'])
IN_PROGRESS = Gauge('http_requests_in_progress', 'HTTP requests in progress')

app = FastAPI(title='Backstract Generated APIs - coll-a2245cc950a44c6ab55715f62508b018', debug=False,
              docs_url='/kind-curie-ecc12b143e1911f0a111be3d1addcd5c32/docs',
              openapi_url='/kind-curie-ecc12b143e1911f0a111be3d1addcd5c32/openapi.json')

FastAPIInstrumentor.instrument_app(app)  # Re-add this line

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router,
    prefix='/kind-curie-ecc12b143e1911f0a111be3d1addcd5c32/api',
    tags=['APIs v1']
)


# Middleware for Prometheus metrics
@app.middleware('http')
async def prometheus_middleware(request: Request, call_next):
    method = request.method
    path = request.url.path
    start_time = time.time()

    IN_PROGRESS.inc()  # Increment in-progress requests

    try:
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time()-start_time)*1000
        status_code = response.status_code
        logger.info(
            f"{request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Time: {process_time:.2f}ms"
        )
    except Exception as e:
        status_code = 500  # Internal server error
        raise e
    finally:
        duration = time.time() - start_time
        REQUEST_COUNT.labels(method=method, endpoint=path,
                             http_status=status_code).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=path,
                               http_status=status_code).observe(duration)
        IN_PROGRESS.dec()  # Decrement in-progress requests

    return response


# Prometheus' metrics endpoint
prometheus_app = make_asgi_app()
app.mount('/metrics', prometheus_app)

# Loki settings
# Update if needed
LOKI_URL = "http://loki.monitoring.svc.cluster.local:3100/loki/api/v1/push"
LOKI_LABELS = {"app": "fastapi-app"}  # Optional labels

# Configure Loguru to send logs to Loki
loki_handler = logging_loki.LokiQueueHandler(
    Queue(-1),
    url=LOKI_URL,
    tags=LOKI_LABELS,
    # auth=("username", "password"),
    version="1"
)

logger.add(loki_handler, level="INFO")  # Adjust log level as needed


def main():
    uvicorn.run('main:app', host='127.0.0.1', port=7070, reload=True)


if __name__ == '__main__':
    main()
