"""Views for capra_webapp"""
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import UploadFileForm
# Create your views here.

from capra_webapp.helpers import Helpers


def index(request):
    """Test view"""


def upload_geojson(request):
    """View to allow the user to upload a GeoJSON file"""
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            json_data = json.load(request.FILES["file"])
            request.session['json_data'] = json.dumps(json_data)
            Helpers.handle_upload_file(f=request.FILES["file"])
            return HttpResponseRedirect(reverse('map_page'))
    else:
        form = UploadFileForm()
    return render(request, 'capra_webapp/upload.html', {"form": form})


def map_page(request):
    """Render the map with waypoints"""
    initial_markers = request.session.pop('json_data', None)
    return render('capra_webapp/map.html', {'initial_markers': initial_markers})


# def send_instructions(request)
