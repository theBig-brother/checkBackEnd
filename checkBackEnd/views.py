from django.http import HttpResponse


def hello(request):
    # return HttpResponse("Hello world ! ")
    # return render(request, 'hello.html')
    return render(request, 'index.html')


from django.shortcuts import render


def runoob(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'runoob.html', context)
