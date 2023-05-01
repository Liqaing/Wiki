from django.shortcuts import render

from . import util

import markdown
from django.http import HttpResponse

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):

    # Capitalized title from input in url
    title = str(title).capitalize()

    # get entry from encyclopedia using get_entry function
    entry = util.get_entry(title)
    
    # check if entry not exist
    if entry == None:
        # give entry variabe a markdown text
        entry = f"# Error 404 \n **{title}** Does Not Exist"

    # convert markdown file into HTML
    entry = markdown.markdown(entry)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry
    })

def search_entry(request):
    if request.method == "POST":

        # Get the input from HTML form
        title = str(request.POST.get("q"))

        # Get entry from encyclopedia
        entry = util.get_entry(title)

        # If title doesn't exist in encycopedia
        if entry == None:

            # Get all entries name
            entries_list = util.list_entries()

            # Create new list to store entry that have title as substring
            new_entries_list = []

            # Check if any entries name has title as its substring
            for entry in entries_list:
                if title.lower() in entry.lower():
                    new_entries_list.append(entry)

            return render(request, "encyclopedia/index.html", {
                "entries": new_entries_list
            })
        
        # Capitalized title
        title = title.capitalize()

        # Convert markdown file into Html
        entry = markdown.markdown(entry)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry
    })