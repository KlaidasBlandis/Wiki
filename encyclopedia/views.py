from django.shortcuts import render
from markdown2 import Markdown
import re, random

from . import util

def index(request):
    markdowner = Markdown()
    entries = util.list_entries()
    if request.method == "POST":
        input = request.POST['q']
        if input in entries:
            md_page = util.get_entry(input)
            page = markdowner.convert(md_page)
            return render(request, "encyclopedia/page.html", {
                "title": input,
                "page": page
            })
        else:
            input_low = input.lower()
            similars = []
            object1 = re.compile(input_low)
            for entry in entries:
                entryl = entry.lower()
                similar = object1.match(entryl)
                if similar:
                    sim_cap = similar.string
                    similars.append(sim_cap.capitalize())
            return render(request, "encyclopedia/search_res.html", {
                "entries": similars
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    markdowner = Markdown()
    md_page = util.get_entry(title)
    if md_page is not None:
        page = markdowner.convert(md_page)
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "page": page
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })

def create(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        entries = util.list_entries()
        if title in entries:
            return render(request, "encyclopedia/error_1.html", {
                "title": title
            })
        else:
            util.save_entry(title, content)
            return render(request, "encyclopedia/page.html", {
                "title": title,
                "page": content
            })    
    return render(request, "encyclopedia/create.html")   

def edit(request):
    if request.method == "POST":
        content = request.POST['content']
        title = request.POST['title']
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "page": content
        })
    else:
        content = request.GET['page']
        title = request.GET['title']
        util.save_entry(title, content)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
    })

def rand_page(request):
    markdowner = Markdown()
    entries = util.list_entries()
    random_entry = random.choice(entries)
    content = util.get_entry(random_entry)
    page = markdowner.convert(content)

    return render(request, "encyclopedia/page.html", {
        "title": random_entry,
        "page": page
    })
