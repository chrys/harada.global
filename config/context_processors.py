from django.conf import settings


def clerk_context(request):
    """Add Clerk keys to template context."""
    return {
        'clerk_publishable_key': settings.CLERK_PUBLISHABLE_KEY,
    }
