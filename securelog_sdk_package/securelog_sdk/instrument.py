import httpx
from .middleware import SecureLogMiddleware


def instrument(app, api_key: str, base_url: str = "http://localhost:8000/logs") -> None:
    """
    Attach SecureLog to your FastAPI app. Call this once, right after
    creating your app instance. Every request is then monitored automatically.

    Args:
        app:      Your FastAPI app instance.
        api_key:  Your sk_... key from the SecureLog dashboard.
        base_url: Your SecureLog server URL.

    Example:
        from fastapi import FastAPI
        from securelog_sdk import instrument

        app = FastAPI()
        instrument(app, api_key="sk_abc123")
    """
    if not api_key or not api_key.startswith("sk_"):
        raise ValueError(
            "[SecureLog] Invalid API key. Keys start with sk_  — "
            "get yours from the SecureLog dashboard."
        )

    _verify_key_on_startup(api_key, base_url)
    app.add_middleware(SecureLogMiddleware, api_key=api_key, base_url=base_url)
    print(f"[SecureLog] Monitoring active → {base_url}")


def _verify_key_on_startup(api_key: str, base_url: str) -> None:
    try:
        resp = httpx.get(
            f"{base_url.rstrip('/')}/auth/verify-key",
            headers={"x-api-key": api_key},
            timeout=5.0,
        )
        if resp.status_code == 401:
            raise ValueError("[SecureLog] API key is invalid or inactive.")
    except httpx.RequestError:
        print("[SecureLog] Warning: could not reach server at startup — will retry on first request.")