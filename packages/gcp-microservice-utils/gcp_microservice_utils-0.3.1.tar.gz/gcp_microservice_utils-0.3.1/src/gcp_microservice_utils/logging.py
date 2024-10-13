import google.cloud.logging


def setup_cloud_logging() -> None:
    google.cloud.logging.Client()
    handler = google.cloud.logging.handlers.StructuredLogHandler()
    google.cloud.logging_v2.handlers.setup_logging(handler)
