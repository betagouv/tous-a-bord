import json

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from public_website.utils.email_provider import send_webhook_notification_email


@csrf_exempt
@require_POST
def webhook(request):
    payload = json.loads(request.body)
    print(f"- {timezone.now()}: {payload}")
    send_webhook_notification_email(
        payload["to"], message=payload["type_de_l_email_a_envoyer"]
    )
    return HttpResponse("OK", content_type="text/plain")
