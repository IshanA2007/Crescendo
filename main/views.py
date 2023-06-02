from django.shortcuts import render, redirect
from .extras import process
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# from .extras import magenta


def index(request):
    file = None
    returnfile = None
    theme = None
    if request.method == "POST" and "file" in request.FILES:
        file = request.FILES["file"]
        theme = request.POST["theme"]
        if file is not None:
            with open(
                BASE_DIR + "/main/extras/audios/" + file.name, "wb"
            ) as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
    ctx = {"file": file, "retfile": None, "theme": theme}
    return render(
        request,
        "index.html",
        context=ctx,
    )
