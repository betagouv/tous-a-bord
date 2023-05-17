import json

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@csrf_exempt
@require_POST
def webhook(request):
    payload = json.loads(request.body)
    print(f"- {timezone.now()}: {payload}")
    return HttpResponse("OK", content_type="text/plain")
