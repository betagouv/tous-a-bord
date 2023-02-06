from django.shortcuts import render
from public_website.forms import InscritPoleEmploi


# Create your views here.
def index_view(request):
    return render(request, "public_website/index.html", {})


def accessibility_view(request):
    return render(request, "public_website/accessibility.html", {})


def pe_status_view(request):
    inscription_state = None

    if request.method == "POST":
        form = InscritPoleEmploi(request.POST)
        if form.is_valid():
            inscription_state = "Inscrite"

    context = {
        "form": InscritPoleEmploi,
        "inscription_state": inscription_state if inscription_state else None
    }
    return render(request, "public_website/pe_status.html", context)
