from django.shortcuts import render


# simple view for hmtl and css template

def index(request):
    return render(request, 'index.html')

