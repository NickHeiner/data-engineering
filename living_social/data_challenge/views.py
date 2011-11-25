# Create your views here.
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from django.http import HttpResponseRedirect
import csv
from data_challenge.models import Customer, Item, Merchant, Transaction
from django.contrib.auth.decorators import login_required

# This module contains the bulk of my logic. In a more complicated app,
# I would factor this out into a controller and make the view "dumb",
# but since this is so small it seems easier to just keep it all in one file.

class UploadFileForm(forms.Form):
    file  = forms.FileField()

def index(request):
    return render_to_response("index.html")

@login_required
def upload(request):
    if request.method == "POST":
        # TODO: validate that the uploaded file is of the correct form
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handleUploadedFile(request.FILES['file'])
            return HttpResponseRedirect('/success')
        
    return render_to_response("upload.html", {'form': UploadFileForm()}, context_instance=RequestContext(request))

@login_required
def success(request):
    mostRecentTransactions = Transaction.objects.filter(fromMostRecentFile=True)
    revenue = getRevenue(mostRecentTransactions)
    
    for transaction in mostRecentTransactions:
        transaction.fromMostRecentFile = False
        transaction.save()
        
    return render_to_response("success.html", {'revenue': revenue})

def getRevenue(transactions):
    return sum([transaction.quantity * transaction.item.price for transaction in transactions])

def handleUploadedFile(data_to_import):
    for record in list(data_to_import)[1:]:
        parseAndSave(record.split("\t"))
        
def parseAndSave(record):
     """ Record is a string of the form 'Amy Pond    $30 of awesome for $10    10.0    5    456 Unreal Rd    Tom's Awesome Shop' """
     # Use get_or_create because if we've seen this entity before, we don't want to make another one
     customer = Customer.objects.get_or_create(name=record[0])
     item = Item.objects.get_or_create(description=record[1], price=float(record[2]))
     merchant = Merchant.objects.get_or_create(address=record[4], name=record[5])
     
     # Create a new transaction for this row, even if we've seen an identical one before
     transaction = Transaction(customer=customer[0], item=item[0], merchant=merchant[0], quantity=int(record[3]), fromMostRecentFile=True)
     transaction.save()
     
     # return for testing. We could also access the values by looking in the database, but 
     # it seems more straightforward just to return them here. That way, if we see an error in a test that uses these returned values,
     # we don't have to worry about persistence as a possible failure point.
     return customer[0], item[0], merchant[0], transaction