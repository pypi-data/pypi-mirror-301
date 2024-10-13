A Python library providing utilities to simplify the integration of various GCP Cloud services like Cloud Logging, Cloud Trace, and authentication with API Gateway into your microservice applications.

This library aims to reduce the boilerplate code required for instrumenting Python microservices with essential GCP services. It provides convenient wrappers and helper functions for:

- Cloud Logging: Easily log structured data with severity levels and custom attributes.
- Cloud Trace: Automatically trace requests across your microservices, enabling distributed tracing and performance analysis.   
- Authentication: Includes Flask middleware to seamlessly process authentication results from GCP API Gateway, simplifying security integration.

## Installation
```sh
pip install gcp-microservice-utils
```
