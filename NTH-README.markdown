# Nick Heiner's Submission for "Challenge for Software Engineer - Big Data"

## How to set up and run
1. Install Python 2.7 and Django 1.3.1.
1. Go to living_social/settings.py and change ABSOLUTE_PATH_TO_PARENT_DIR according to your setup.
1. Run the server
    C:\Users\Nick\Code\Living Social\data-engineering\living_social>c:\Python27\python.exe manage.py runserver

    Validating models...

    0 errors found
    Django version 1.3.1, using settings 'living_social.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.
1. Go to the specified url for the devserver.

## Notes
In general, I strive to avoid commenting code - ideally it should be clear enough that a comment is unnecessary.
Also, comments risk becoming out of date with the code itself, which is a total mess.
For this coding challenge, I have left more comments, because I'm trying to show you how I think. 

The time breakdown for this task is around:

* 25 minutes to read the description, form a plan, and get Django set up
* 1.5 hours of coding and unit tests to implement the main requirements
* 45 minutes to research Django OpenID plugins and integrate django_openid_auth 
* 25 minutes of writeup and final checking

### Database Schema
The data originally exists in the format: purchaser name, item description, item price, purchase count, merchant address, and merchant name

It seems natural to normalize this out into the following entities:

	Customer: (purchaser name)
	Item: (item description, item price)
	Merchant: (merchant name, merchant address)
	Transaction (customer, item, merchant, purchase count)
	
I assumed that for each entity except a transaction, its attributes uniquely identify it.
(If we see a customer with the name "RedFoo" several times, we have no meaningful way of determining whether this refers to one or many people.)

Conversely, it seems reasonable that the same transaction could occur multiple times, and we'd want to be able to represent that.
 
In the real world, it would probably be important to be able to maintain a persistent identity for a customer or merchant even if they change names or addresses over time.
However, there is no ID in the data provided that would allow us to do this, so I have ommitted it.

### Django and Python
Django and Python are a natural fit for a quick task like this. Django's coding style is beautifully simple. Working with models is fantastically easy - you declaratively
specify fields you want, and which database backend you want to use, and it handles the rest through a clean get() and put() interface. The templating system is also quite nice - 
its inheritence system makes code reuse easy. It's clear that Django's designers thought carefully about how to design a powerful, modern web framework that gets out of your way
and lets you prototype quickly.

I wrote ample unit tests. Particularly in a language like Python that doesn't offer any form of compile-time safety, it's important to make sure every code path is getting hit.

I used a simple Django library, django_openid_auth, to support OpenID authentication. In the real world, I wouldn't make the user manually copy/paste their OpenID endpoint
into a textbox, but forking django_openid_auth to create an aesthetically pleasing OpenID provider picker seems beyond the scope of this challenge.

### Ideas for further improvement
* Implement a HTML5 drag-and-drop AJAX uploader
* Implement a better way to show validation errors in the input file (pointing to specific lines)
* Show revenue totals from previous uploads
