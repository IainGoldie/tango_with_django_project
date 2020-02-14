from rango.models import Page
from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.forms import CategoryForm 
from django.shortcuts import redirect

def add_category(request):
    form = CategoryForm()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)
            
    return render(request, 'rango/add_category.html', {'form': form})
    

def show_category(request, category_name_slug): 
# Create a context dictionary which we can pass 
# to the template rendering engine. 
    context_dict = {}

    try:
    # Can we find a category name slug with the given name? 
    # If we can't, the .get() method raises a DoesNotExist exception. 
    # The .get() method returns one model instance or raises an exception. 
        category = Category.objects.get(slug=category_name_slug)

    # Retrieve all of the associated pages. 
    # The filter() will return a list of page objects or an empty list. 
        pages = Page.objects.filter(category=category)
    # Adds our results list to the template context under name pages. 
        context_dict['pages'] = pages 
    # We also add the category object from 
    # the database to the context dictionary. 
    # We'll use this in the template to verify that the category exists. 
        context_dict['category'] = category 
    except Category.DoesNotExist: 
    # We get here if we didn't find the specified category. 
    # Don't do anything 
    # the template will display the "no category" message for us. 
        context_dict['category'] = None 
        context_dict['pages'] = None
# Go render the response and return it to the client. 
    return render(request, 'rango/category.html', context=context_dict)


def index(request):
    
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('views')[:5]

    # Construct a dictionary to pass to the template engine as its context. 
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

# Return a rendered response to send to the client. 
# We make use of the shortcut function to make our lives easier. 
# Note that the first parameter is the template we wish to use. 
    return render(request, 'rango/index.html', context=context_dict)

    
    #html = '<a href="/rango/about/">About</a>'
    #return HttpResponse("Rango says hello there partner!" + html)
    
def about(request):
    context_dict = {'author': 'This website was created by Iain Goldie'}
    return render(request, 'rango/about.html', context=context_dict)
    
    html = '<a href="/rango/">Home Page</a>'
    return HttpResponse("Rango says here is the about page." + html)
    
