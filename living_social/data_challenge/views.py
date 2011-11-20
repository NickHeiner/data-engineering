# Create your views here.
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext

class UploadFileForm(forms.Form):
    file  = forms.FileField()

def index(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success')
        
    return render_to_response("index.html", {'form': UploadFileForm()}, context_instance=RequestContext(request))

def success(request):
    return render_to_response("success.html")