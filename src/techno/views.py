from django.shortcuts import render


# simple view for hmtl and css template

def index(request):
    return render(request, 'blog/postList.html')

def postview(request):
    return render(request, 'blog/postView.html')
