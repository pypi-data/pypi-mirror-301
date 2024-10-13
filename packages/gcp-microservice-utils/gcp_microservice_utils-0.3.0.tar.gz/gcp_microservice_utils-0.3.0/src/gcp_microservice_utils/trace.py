import random
from flask import Flask, current_app, request, g, request_tearing_down
from datetime import datetime, timezone
import google.auth
from google.cloud.trace_v2 import TraceServiceClient, Span
from google.cloud.trace_v2.types import TruncatableString
from google.protobuf.timestamp_pb2 import Timestamp

def _truncate_str(str_to_check, limit):
    """Check the length of a string. If exceeds limit, then truncate it."""
    encoded = str_to_check.encode("utf-8")
    truncated_str = encoded[:limit].decode("utf-8", errors="ignore")
    return truncated_str, len(encoded) - len(truncated_str.encode("utf-8"))

class TraceSpan:
    def __init__(self, display_name):
        self.display_name = display_name

    def __enter__(self):
        if not hasattr(current_app, 'cloud_trace_client'):
            return

        if 'trace_ignore' in g and g.trace_ignore == True:
            return

        if not 'Traceparent' in request.headers:
            g.trace_ignore = True
            return
            
        parts = request.headers['Traceparent'].split('-')
        if len(parts) != 4:
            g.trace_ignore = True
            return
        
        version, trace_id, parent_span_id, flags = parts

        flags = int(flags, 16)

        if version != '00':
            g.trace_ignore = True
            return

        if (flags & 1) == 0:
            # This request is not sampled
            g.trace_ignore = True
            return

        if not 'spans' in g:
            g.spans = list()
            g.spans_level = 0

        if len(g.spans) > 0:
            parent_span_id = g.spans[-1]['span_id']

        span_id = random.getrandbits(64)
        span_id = f"{span_id:016x}"

        g.spans.append({
            'display_name': self.display_name,
            'trace_id': trace_id,
            'span_id': span_id,
            'parent_span_id': parent_span_id,
            'start_time': int(datetime.now(timezone.utc).timestamp() * 1e9)
        })

        g.spans_level = g.spans_level + 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not hasattr(current_app, 'cloud_trace_client'):
            return

        if 'trace_ignore' in g and g.trace_ignore == True:
            return

        g.spans_level = g.spans_level - 1

        span = g.spans[g.spans_level]
        span['end_time'] = int(datetime.now(timezone.utc).timestamp() * 1e9)
        g.spans[g.spans_level] = span

def _send_traces(sender, **extra):
    if not 'spans' in g:
        return

    gcp_spans = list()

    for span in g.spans:
        ts_start = Timestamp()
        ts_start.FromNanoseconds(span['start_time'])

        ts_end = Timestamp()
        ts_end.FromNanoseconds(span['end_time'])

        truncated, truncated_byte_count = _truncate_str(span['display_name'], 128)

        gcp_span = Span(
            name=f"projects/{current_app.cloud_trace_project_id}/traces/{span['trace_id']}/spans/{span['span_id']}",
            span_id=span['span_id'],
            parent_span_id=span['parent_span_id'],
            display_name=TruncatableString(value=truncated, truncated_byte_count=truncated_byte_count),
            start_time=ts_start,
            end_time=ts_end
        )

        gcp_spans.append(gcp_span)

    current_app.cloud_trace_client.batch_write_spans(
        name=f"projects/{current_app.cloud_trace_project_id}",
        spans=gcp_spans
    )

def trace_function(display_name: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with TraceSpan(display_name):
                return func(*args, **kwargs)
        return wrapper
    return decorator

def setup_cloud_trace(app: Flask) -> None:
    app.cloud_trace_client = TraceServiceClient()
    _, app.cloud_trace_project_id = google.auth.default()

    request_tearing_down.connect(_send_traces, app)
