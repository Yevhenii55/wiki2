from django.shortcuts import render, redirect, HttpResponseRedirect
import markdown
from . import util
from .util import get_entry
from .util import save_entry
from .util import list_entries
from django.urls import reverse
import urllib.parse

from random import choice
import sys



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })







def entry(request, title):
    # Отримання вмісту статті за назвою `title`
    content = get_entry(title)

    if content is None:
        # Якщо стаття не знайдена, повернути сторінку з повідомленням про відсутність
        return render(request, "encyclopedia/not_found.html")

    # Перетворення вмісту статті з Markdown в HTML
    content_html = markdown.markdown(content)

    # Декодування рядка `title` з 'utf-8'
    title = urllib.parse.unquote(title)
    # Передача даних у шаблон `entry.html`
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content_html,
    })



def search(request):
    if request.method == "GET":
        query = request.GET.get('q')
        entry = get_entry(query)
        if entry:
            return redirect('entry', title=query)
        else:
            entries = list_entries()
            search_results = [entry for entry in entries if query.lower() in entry.lower()]
            return render(request, "encyclopedia/search.html", {
                "query": query,
                "search_results": search_results
            })
        



def new_page(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        existing_entry = get_entry(title)
        if existing_entry:
            return render(request, "encyclopedia/error.html", {
                "error_message": "An entry with that title already exists."
            })
        else:
            with open(f"entries/{title}.md", "w", encoding="utf-8") as f:
                f.write(content)
            return redirect('entry', title=title)
    else:
        return render(request, "encyclopedia/new_page.html")






def edit_page(request, title):
    # Отримати наявний контент сторінки
    current_content = get_entry(title)

    if request.method == 'POST':
        # Отримати новий контент з форми
        new_content = request.POST.get('content')

        # Оновити контент сторінки
        with open(f"entries/{title}.md", "w", encoding="utf-8") as f:
            f.write(new_content)

        # Перенаправити користувача назад на сторінку цієї статті
        return redirect('entry', title=title)

    return render(request, 'encyclopedia/edit_page.html', {
        'title': title,
        'content': current_content,
    })



def random_page(request):
    entries = list_entries()
    random_title = choice(entries)
    return redirect('entry', title=random_title)





