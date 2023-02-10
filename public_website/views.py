from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from public_website.decorators import belongs_to_group

from public_website.forms import InscritPoleEmploi
from public_website.models import APICall


def index_view(request):
    return render(request, "public_website/index.html", {})


def accessibility_view(request):
    return render(request, "public_website/accessibility.html", {})


def login_view(request):
    return render(request, "public_website/login.html", {})

@user_passes_test(belongs_to_group("Artois Mobilités"))
def pe_status_view(request):
    inscription_data = None
    form = InscritPoleEmploi

    if request.method == "POST":
        form = InscritPoleEmploi(request.POST)
        if form.is_valid():
            call = APICall(
                user=request.user,
                queried_id=form.cleaned_data["identifiantPE"],
                url=request.get_full_path(),
            )
            response = call.fetch()
            call.save()

            inscription_data = response.json()

    context = {
        "form": form,
        "inscription_data": inscription_data,
    }
    return render(request, "public_website/pe_status.html", context)
