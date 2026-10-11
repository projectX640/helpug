from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner


WS_TOKEN_MAX_AGE = 15 * 60
PUBLIC_CHAT_TOKEN_MAX_AGE = 48 * 60 * 60
_signer = TimestampSigner(salt="incidents.websocket.access")
_public_chat_signer = TimestampSigner(salt="incidents.public_chat.access")


def make_websocket_token(kind, allowed_ids, user_id=None, sender_type=None):
    return _signer.sign_object({
        "kind": kind,
        "allowed_ids": [int(value) for value in allowed_ids],
        "user_id": user_id,
        "sender_type": sender_type,
    })


def make_public_chat_token(incident):
    return _public_chat_signer.sign_object({
        "kind": "public_emergency_chat",
        "incident_id": incident.pk,
        "request_id": incident.request.request_id,
    })


def public_chat_token_identity(token):
    if not token:
        return None
    try:
        return _public_chat_signer.unsign_object(token, max_age=PUBLIC_CHAT_TOKEN_MAX_AGE)
    except (BadSignature, SignatureExpired, ValueError, TypeError):
        return None


def public_chat_token_matches(token, incident):
    identity = public_chat_token_identity(token)
    if identity is None:
        return False
    return (
        identity.get("kind") == "public_emergency_chat"
        and identity.get("incident_id") == incident.pk
        and identity.get("request_id") == incident.request.request_id
    )


class WebSocketTokenMiddleware:
    def __init__(self, inner):
        self.inner = inner
        self.authenticated_inner = AuthMiddlewareStack(inner)

    async def __call__(self, scope, receive, send):
        token = parse_qs(scope.get("query_string", b"").decode("utf-8")).get("token", [""])[0]
        try:
            identity = _signer.unsign_object(token, max_age=WS_TOKEN_MAX_AGE)
        except (BadSignature, SignatureExpired, ValueError, TypeError):
            await send({"type": "websocket.close", "code": 4403})
            return
        scope = dict(scope)
        scope["websocket_identity"] = identity
        if identity.get("user_id") is not None:
            await self.authenticated_inner(scope, receive, send)
            return
        await self.inner(scope, receive, send)
