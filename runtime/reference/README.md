# Reference API Runtime

`server.py` is a deliberately small local reference implementation of the alpha1.0 API.

## Run

```bash
python runtime/reference/server.py
```

The server binds to `127.0.0.1:8000` only.

## Important boundary

This runtime stores data in process memory and is **not production-ready**. It has no authentication, authorization, encryption, durable database, audit trail, rate limiting, backup, or safeguarding workflow integration.

In particular, anonymous reports and safeguarding signals require stronger controls before real use. The API can draft and organize information, but professional, safeguarding, legal, medical, and childcare decisions remain with authorized humans and applicable procedures.
