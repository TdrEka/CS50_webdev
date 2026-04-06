from django.shortcuts import redirect, render
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"{title} page was not found."
        })
    import markdown2
    content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })
    
def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()
    if query.lower() in [e.lower() for e in entries]:
        return redirect(f"/wiki/{query}")
    
    results = [e for e in entries if query.lower() in e.lower()]
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })
    
def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect(f"/wiki/{random_entry}")

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "message": f"'{title}' already exists!"
            })
        
        util.save_entry(title, content)
        return redirect(f"/wiki/{title}")
    
    return render(request, "encyclopedia/new.html")

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("content", "")
        util.save_entry(title, content)
        return redirect(f"/wiki/{title}")
    
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })