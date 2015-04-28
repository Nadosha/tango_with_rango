from django.shortcuts import render
from django.http import HttpResponse

# 4.7. Exercises
def index(request):
	#Revise the HttpResponse in the index view to include a link to the about page.
    #return HttpResponse("Rango says hello baby! <br/> <a href='/rango/about'>About Rango</a>")

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I bold font the context"}
    # Return a rendered response to send to the client.
    return render(request, 'rango/index.html', context_dict)


# Now create a new view called about which returns the following: Rango says here is the about page.
def about(request):
	#In the HttpResponse in the about view include a link back to the main page.
	return HttpResponse("Rango says here is the about page <br/> <a href='/rango/'>Back to Index page</a>")