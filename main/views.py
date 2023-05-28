from django.shortcuts import render, redirect
from .extras import process

# from .extras import magenta


def index(request):
    file = None
    returnfile = None
    if request.method == "POST" and "file" in request.FILES:
        file = request.FILES["file"]

    ctx = {
        "file": file,
        "retfile": returnfile,
    }
    return render(
        request,
        "index.html",
        context={"file": file},
    )
