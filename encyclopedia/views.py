from django.shortcuts import render

from . import util

# Module that I have imported
import markdown
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from django.shortcuts import redirect

#  New class for a form that use to create new entry
class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title", widget=forms.TextInput(attrs={"class": "col-12", "placeholder":"Entry Title"}))
    entry_content = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control col-12", "rows":"12", "placeholder":"Entry Content"}))

# Search function to search if entry title is already exist in entry list, specify that the parameter of the function is a string and entries list 
def search_title(title: str, list_entries):
    # Check if the tile provided exist in list of entries title case-insensitively
    if title.casefold() in (entry_title.casefold() for entry_title in list_entries):
        # Return true if title existed else return false
        return True
    return False

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):

    # Capitalized title from input in url
    title = str(title).upper()
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
    # If form is submitted
    if request.method == "POST":
        # Get the input from the form
        title = str(request.POST.get("q")).upper()
        # Get all entries list name
        list_entries = util.list_entries()
        # Check if title is exist in the list of entries name
        if search_title(title, list_entries):
            # If true (title exist in list entries) redirect user to that entry page
            return redirect(reverse("entry_page", kwargs={'title':title}))
        
        # If not, find all entries name which have that title as its substring
        # Create new list to store all entry that have title as substring
        new_list_entries = []
        # Check for every entry name in the list entries to find which entry name has title as its substring
        for entry in list_entries:
            if title.casefold() in entry.casefold():
                # For every entry name that do, add that entry name to the new list entries
                new_list_entries.append(entry)

        # If there is no entry with title as its substring
        if not new_list_entries:
            # Show Error 404 message
            message = f"# Error 404 \n **{title}** Does Not Exist"
            message = markdown.markdown(message)
            # Render Error message
            return render(request, "encyclopedia/none_exist.html", {
                "content": message
            })
        
        # Render new list entries that have input title as its substring back
        return render(request, "encyclopedia/index.html", {
            "entries": new_list_entries
        })

            


# def search_entry(request):
#     if request.method == "POST":
#         # Get the input from HTML form
#         title = str(request.POST.get("q"))
#         # Get entry from encyclopedia
#         entry = util.get_entry(title)
#         # If title doesn't exist in encycopedia
#         if entry == None:
#             # Get all entries name
#             entries_list = util.list_entries()
#             # Create new list to store entry that have title as its substring
#             new_entries_list = []
#             # Check if any entries name has title as its substring
#             for entry in entries_list:
#                 if title.lower() in entry.lower():
#                     new_entries_list.append(entry)
#             # If there is no entry with title as substring
#             if not new_entries_list:
#                 # Show Error 404 message
#                 message = f"# Error 404 \n **{title}** Does Not Exist"
#                 message = markdown.markdown(message)

#                 return render(request, "encyclopedia/none_exist.html", {
#                     "content": message
#                 })
            
#             return render(request, "encyclopedia/index.html", {
#                 "entries": new_entries_list
#             })
#         # Capitalized title
#         title = title.capitalize()
#         # Convert markdown file into Html
#         entry = markdown.markdown(entry)

#     return render(request, "encyclopedia/entry.html", {
#         "title": title,
#         "entry": entry
#     })

def create_new_entry(request):
    # If form is submitted through POST request
    if request.method == "POST":
        # Create new form variable and fill it with data that was submit
        form = NewEntryForm(request.POST)
        # Check if form is valid
        if form.is_valid():
            # Get the entry title that was submitted
            title = form.cleaned_data["title"]
            # Check if that entry title is an already existed entry title in list entries
            if search_title(title, list_entries=util.list_entries()):
                # Return error message back
                return render(request, "encyclopedia/create_new_entry.html",{
                    "form": form,
                    # Provided error message to display to user
                    "title_error": "This entry title is already exist, try other title."
                })
            
            # If there is no problem with submitted form, then save the entry
            # Get entry content from the submmited form
            entry_content = form.cleaned_data["entry_content"]
            # Save the entry content to disk
            util.save_entry(title, entry_content)

            # Redirect to new entry page, Redirect to a dynamic url
            return redirect(reverse("entry_page",kwargs={'title':str(title)}))

        # If form is not valid, then send back existing form data along with error message
        return render(request, "encyclopedia/create_new_entry.html", {
            "form": form
        })

    return render(request, "encyclopedia/create_new_entry.html", {
        "form": NewEntryForm
    })