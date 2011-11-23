# Create your views here.
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from django.http import HttpResponseRedirect
import csv
from data_challenge.models import Customer, Item, Merchant, Transaction
from django.contrib.auth.decorators import login_required

class UploadFileForm(forms.Form):
    file  = forms.FileField()

def index(request):
    return render_to_response("index.html")

@login_required
def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handleUploadedFile(request.FILES['file'])
            return HttpResponseRedirect('/success')
        
    return render_to_response("upload.html", {'form': UploadFileForm()}, context_instance=RequestContext(request))

@login_required
def success(request):
    revenue = getRevenue(Transaction.objects.all())
    return render_to_response("success.html", {'revenue': revenue})

def getRevenue(transactions):
    return sum([transaction.quantity * transaction.item.price for transaction in transactions])

def handleUploadedFile(data_to_import):
    for record in list(data_to_import)[1:]:
        parseAndSave(record.split("\t"))
        
def parseAndSave(record):
     """ Record is a string of the form 'Amy Pond    $30 of awesome for $10    10.0    5    456 Unreal Rd    Tom's Awesome Shop' """
     customer = Customer.objects.get_or_create(name=record[0])
     item = Item.objects.get_or_create(description=record[1], price=float(record[2]))
     merchant = Merchant.objects.get_or_create(address=record[4], name=record[5])
     transaction = Transaction.objects.get_or_create(customer=customer[0], item=item[0], merchant=merchant[0], quantity=int(record[3]))
     
     # return for testing. We could also access the values by looking in the database, but 
     # it seems more straightforward just to return them here. That way, if we see an error in a test that uses these returned values,
     # we don't have to worry about persistence as a possible failure point.
     return customer[0], item[0], merchant[0], transaction[0]