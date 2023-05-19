import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from public_website.utils.email_provider import send_webhook_notification_email


@csrf_exempt
@require_POST
def webhook(request):
    payload = json.loads(request.body)
    send_webhook_notification_email(payload)
    return HttpResponse("OK", content_type="text/plain")
