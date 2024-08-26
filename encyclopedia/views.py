from django.shortcuts import render
import markdown2
import random
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def convert(request, title ):
    
    content = util.get_entry(title)
    
    if content == None:
        return render(request, 'encyclopedia/error.html', {
         'mensaje': "La entrada no existe."
        })
        
    else:
        html_convert = markdown2.markdown(content)
        
        return render(request, 'encyclopedia/entry.html',
        {
            'title':title,
            'html_convert':html_convert,             
        })

def search(request):
    if request.method == "POST":
        
        search  = request.POST['q']
    
        content = util.get_entry(search)
        
        if content is not None :
            html = markdown2.markdown(content)
            return render(request , "encyclopedia/entry.html",{
                "title" : search,
                "html_search":html,
            })
        else:
            all_entry = util.list_entries()
            recomendation = []
            for entry in all_entry:
                if search.lower() in entry.lower():
                    recomendation.append(entry)
            return render(request,"encyclopedia/search.html",{
                'recomendation': recomendation
                })

def new_page(request):
    if request.method == "GET":
        return render(request,"encyclopedia/new_page.html")
    else:
        
        title = request.POST['title']
        content = request.POST['content']

        title_exist = util.get_entry(title)
        
        if title_exist is not None:
            return render(request, "encyclopedia/error.html",{
                'mensaje':"Esta pagina ya existe."
                })
        else:
            header_title = f"#{title}"
            pass_mk = header_title + content
             
            util.save_entry(title,pass_mk)
           
            content = util.get_entry(title)
            if content == None:
                return render(request, 'encyclopedia/error.html', {
                'mensaje': "Fallo tecnico."
                })
                
            else:
                html_convert = markdown2.markdown(content)
                
                return render(request, 'encyclopedia/entry.html',
                {
                    'title':title,
                    'html_convert':html_convert,             
                })

def edit(request):
    if request.method == "POST":
        title = request.POST["entry_title"]
        content = util.get_entry(title)

        return render(request,"encyclopedia/edit.html",{
            "title":title,
            "content":content,       
             })

def save(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']

        util.save_entry(title,content)
        
        content = util.get_entry(title)
        
        if content == None:
            
            return render(request, 'encyclopedia/error.html', {
                'mensaje': "Fallo tecnico."
                })
                
        else:
                html_convert = markdown2.markdown(content)
                
        return render(request, 'encyclopedia/entry.html',
                {
                    'title':title,
                    'html_convert':html_convert,             
                })

def random_page(request):
    entry = util.list_entries()
    rand_entry = random.choice(entry)

    content = util.get_entry(rand_entry)
    
    if content == None:
        return render(request, 'encyclopedia/error.html', {
         'mensaje': "La entrada no existe."
        })
        
    else:
        html_convert = markdown2.markdown(content)
        
        return render(request, 'encyclopedia/entry.html',
        {
            'title':rand_entry,
            'html_convert':html_convert,             
        })