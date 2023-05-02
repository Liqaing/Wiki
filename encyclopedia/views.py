from django.shortcuts import render

from . import util

# Module that I have imported
import markdown
from django.http import HttpResponse
from django import forms

#  New class for a form that use to create new entry
class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title")
    entry_content = forms.CharField(widget=forms.Textarea(attrs={"rows":"1", "cols":"40"}))

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

        # Convert markdown file into HTML
        entry = markdown.markdown(entry)

        # Render Error 404 page
        return render(request, "encyclopedia/none_exist.html", {
            "content": entry
        })

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

            # If there is no entry with title as substring
            if not new_entries_list:
                # Show Error 404 message
                message = f"# Error 404 \n **{title}** Does Not Exist"
                message = markdown.markdown(message)

                return render(request, "encyclopedia/none_exist.html", {
                    "content": message
                })

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

def create_new_entry(request):

    return render(request, "encyclopedia/create_new_entry.html", {
        "form": NewEntryForm
    })