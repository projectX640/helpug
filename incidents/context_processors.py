from django.db.models import Q

from .models import Incident


def dashboard_navigation(request):
    if not request.user.is_authenticated or not request.user.is_active:
        return {}

    if request.user.is_superuser and not hasattr(request.user, "response_profile"):
        visible_incidents = Incident.objects.all()
    else:
        profile = getattr(request.user, "response_profile", None)
        if profile is None or not profile.active:
            return {}
        assigned_areas = profile.areas.filter(active=True)
        visible_incidents = Incident.objects.filter(
            Q(assigned_area__in=assigned_areas)
            | Q(referrals__recipient_admin=request.user)
        ).distinct()

    incoming = visible_incidents.filter(status="new", opened_at__isnull=True)
    severity = "normal"
    for priority in ("critical", "high", "medium"):
        if incoming.filter(request__priority=priority).exists():
            severity = priority
            break

    return {
        "dashboard_nav_count": incoming.count(),
        "dashboard_nav_severity": severity,
    }
