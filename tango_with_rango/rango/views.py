from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm

# 4.7. Exercises
def index(request):
	#Revise the HttpResponse in the index view to include a link to the about page.
    #return HttpResponse("Rango says hello baby! <br/> <a href='/rango/about'>About Rango</a>")

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    # Return a rendered response to send to the client.
    return render(request, 'rango/index.html', context_dict)


# Now create a new view called about which returns the following: Rango says here is the about page.
def about(request):
	#In the HttpResponse in the about view include a link back to the main page.
	return render(request, 'rango/about.html')

def category(request, category_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)

def add_category(request):
	# A HTTP POST ?
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			# Save the new ctegory to the database
			form.save(commit=True)
			return index(request)
		else:
			print form.errors
	else:
		# If the request was not a POST, display the form to enter details.
		form = CategoryForm()

	return render(request, 'rango/add_category.html', {'form': form})

from rango.forms import PageForm

def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)

