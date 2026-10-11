import logging

from django.conf import settings
from django.db import DatabaseError

from .models import SecurityEvent


logger = logging.getLogger(__name__)


def request_ip(request):
    if settings.TRUST_PROXY_HEADERS:
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if forwarded_for:
            return forwarded_for.split(",", 1)[0].strip() or None
    return request.META.get("REMOTE_ADDR") or None


def record_security_event(request, event_type, user=None, details=None):
    try:
        return SecurityEvent.objects.create(
            event_type=event_type,
            user=user if getattr(user, "is_authenticated", False) else None,
            ip_address=request_ip(request),
            path=request.path[:255],
            method=request.method[:10],
            details=details or {},
        )
    except DatabaseError:
        logger.exception("Could not persist security event: %s", event_type)
        return None
