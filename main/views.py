from django.shortcuts import render, redirect
from .extras import process
import os

# from .extras import magenta


def index(request):
    file = None
    returnfile = None
    if request.method == "POST" and "file" in request.FILES:
        file = request.FILES["file"]
    file_path = os.path.join("extras/audios", file.name)  # Construct the file path

    with open(file_path, "wb") as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    ctx = {
        "file": file,
        "retfile": returnfile,
    }
    return render(
        request,
        "index.html",
        context={"file": file},
    )
