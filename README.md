# Cost‑Aware Model Serving

This project demonstrates a simple routing layer that selects among
multiple large language model providers based on cost and latency
considerations.  It exposes a single `/generate` HTTP endpoint and
forwards requests to the cheapest provider that satisfies the user’s
latency constraint.

## Features

- Pluggable providers with configurable cost per token and average
  latency.
- Basic caching of recent responses to avoid redundant calls.
- Simple fallback mechanism in case a provider returns an error.
- Easily extensible: add new providers by subclassing `BaseProvider`.

## Usage

Install dependencies and run the service:

```bash
pip install -r requirements.txt
python router.py
```

Send a POST request to `http://localhost:8000/generate` with JSON
containing a prompt and optional max_tokens and desired_latency fields.

## Extending

To add a new model provider, create a subclass of `BaseProvider` in
`providers.py` implementing the `generate` method and specifying cost
and latency attributes.  Then register it in `Router.__init__`.