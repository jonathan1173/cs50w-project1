from django.shortcuts import render
import markdown2

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def convert(request, title ):
    
    content = util.get_entry(title)
    
    if content == None:
        return render(request, 'encyclopedia/error.html', {
         'error': "La entrada no existe."
        })


    else:
        html_convert = markdown2.markdown(content)
        
        return render(request, 'encyclopedia/entry.html',
        {
            'title':title,
            'html_convert':html_convert,
                          
        })

