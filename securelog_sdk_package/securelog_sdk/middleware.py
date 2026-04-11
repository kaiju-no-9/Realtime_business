import time
import asyncio
import httpx
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class SecureLogMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, api_key: str, base_url: str):
        super().__init__(app)
        self.api_key  = api_key
        self.base_url = base_url.rstrip("/")
        self._client  = None

    async def dispatch(self, request: Request, call_next):
        start    = time.monotonic()
        response = await call_next(request)
        elapsed  = round((time.monotonic() - start) * 1000, 2)

        payload = self._build_payload(request, response, elapsed)
        asyncio.create_task(self._send(payload))

        return response

    def _build_payload(self, request: Request, response, elapsed_ms: float) -> dict:
        actor_email, actor_id, actor_role = self._extract_actor(request)
        return {
            "event_type":           _infer_event_type(request.method, request.url.path),
            "actor_email":          actor_email,
            "actor_id":             actor_id,
            "actor_role":           actor_role,
            "ip_address":           _get_ip(request),
            "user_agent":           request.headers.get("user-agent"),
            "endpoint":             str(request.url.path),
            "method":               request.method,
            "status_code":          response.status_code,
            "response_time_ms":     elapsed_ms,
            "privilege_escalation": _is_priv_escalation(request.url.path, response.status_code),
            "severity":             _infer_severity(response.status_code),
        }

    def _extract_actor(self, request: Request):
        user = getattr(request.state, "user", None)
        if not user:
            return None, None, None
        return (
            getattr(user, "email", None),
            str(getattr(user, "id", "") or "") or None,
            getattr(user, "role", None),
        )

    async def _send(self, payload: dict):
        try:
            if self._client is None:
                self._client = httpx.AsyncClient(timeout=3.0)
            await self._client.post(
                f"{self.base_url}/logs",
                json=payload,
                headers={"x-api-key": self.api_key},
            )
        except Exception:
            pass


def _infer_event_type(method: str, path: str) -> str:
    p = path.lower()
    if any(x in p for x in ("login", "signin")):        return "login"
    if any(x in p for x in ("logout", "signout")):      return "logout"
    if any(x in p for x in ("register", "signup")):     return "register"
    if "password" in p:                                   return "password_change"
    if any(x in p for x in ("role", "permission")):     return "role_change"
    if "admin" in p:                                      return "admin_action"
    if any(x in p for x in ("export", "download")):     return "file_download"
    if "delete" in p or method == "DELETE":              return "delete"
    return {"POST": "create", "PUT": "update", "PATCH": "update", "GET": "read"}.get(method, "api_call")


def _infer_severity(code: int) -> str:
    if code >= 500:             return "high"
    if code in (401, 403):      return "medium"
    return "low"


def _is_priv_escalation(path: str, code: int) -> bool:
    p = path.lower()
    return code < 300 and any(x in p for x in ("role", "permission", "admin"))


def _get_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"