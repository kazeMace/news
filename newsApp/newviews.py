from django.shortcuts import render


def newindex(request):
    context = {}
    return render(request, 'newindex.html', context)