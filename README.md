# Cost-aware model serving

A FastAPI routing example that selects the cheapest configured adapter whose
declared average latency meets the request. The bundled adapters return
synthetic text and use illustrative costs and latency estimates.

## Run the example

```bash
python -m pip install -r requirements.txt
python -m uvicorn router:app --host 127.0.0.1 --port 8000
curl -X POST http://127.0.0.1:8000/generate -H "Content-Type: application/json" -d '{"prompt":"hello","max_tokens":5,"desired_latency":0.5}'
```

The default registry selects `EchoProvider` and returns `hello`. It has
the lowest declared cost and latency, so other adapters can be compared by
passing a custom registry to `Router`. A request with an infeasible latency
returns HTTP 400. An explicitly empty registry raises a clear error.

The example truncates characters using the historical `max_tokens` parameter.
A real provider adapter would implement its model's token limits. Latency
values are selection metadata. Caching and provider fallback remain possible
extensions.

## Verify

```bash
python -m pip install pytest
python -m pytest -q
```

## Deployment verification

Use Python 3.12 on Linux. CI and the container use the checked-in dependency constraints.

```sh
python -m pip install -c requirements.lock -r requirements-dev.txt
python -m pytest -q
docker build -t reviewer-smoke .
docker run --rm -p 127.0.0.1:8000:8000 reviewer-smoke
```

The container serves the API docs at `http://127.0.0.1:8000/docs`. Use the local example above to exercise its main route. The router uses fixture providers and illustrative cost and latency settings.
