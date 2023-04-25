from django.shortcuts import render

from . import util

import markdown
from django.http import HttpResponse

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):

    # Capitalized title from input
    title = str(title).capitalize()

    # get entry from encyclopedia using get_entry function
    entry = util.get_entry(title)
    
    # check if entry not exist
    if entry == None:
        # give entry variabe a markdown text
        entry = f"**{title}** Does Not Exist"

    # convert markdown file into HTML
    entry = markdown.markdown(entry)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry
    })