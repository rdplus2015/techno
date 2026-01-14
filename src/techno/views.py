from django.shortcuts import render


# simple view for hmtl and css template

def index(request):
    return render(request, 'post/postList.html')

def postview(request):
    return render(request, 'post/postView.html')
