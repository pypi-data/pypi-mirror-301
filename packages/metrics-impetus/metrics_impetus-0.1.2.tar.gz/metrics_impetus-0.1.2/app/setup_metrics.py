from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
import newrelic.agent

def setup_instrumentation(app, config):

    # Instrument the FastAPI app with Prometheus metrics for default metrics as well as exposing /metrics 
    Instrumentator().instrument(app).expose(app)

    # Instrument the FastAPI app with OpenTelemetry for Http requests
    FastAPIInstrumentor.instrument_app(app)

    # Configure logging instrumentation with OpenTelemetry
    LoggingInstrumentor(set_logging_format=True)

    # Initialize Sentry for error tracking
    # sentry_sdk.init(
    #     dsn=config.SENTRY_DSN,
    #     traces_sample_rate=1.0,
    #     profiles_sample_rate=1.0,
    # )

    # Add Sentry middleware
    app.add_middleware(SentryAsgiMiddleware)

    # Initialize New Relic agent for application performance monitoring
    newrelic.agent.initialize()

