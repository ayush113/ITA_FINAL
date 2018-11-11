from django.shortcuts import render

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import connection
from notes.utils import namedtuplefetchall
from django.contrib.auth.decorators import login_required

@login_required
def simple_upload(request):
    with connection.cursor() as curr:
        curr.execute("select filename,shared_url,first_name,last_name from fileshared inner join auth_user on fileshared.user_id = auth_user.id")
        results = namedtuplefetchall(curr)

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        data = request.POST
        data = data.get('filename')
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        with connection.cursor() as curr:
            curr.execute("INSERT INTO fileshared(filename,user_id, shared_url) VALUES (%s,%s,%s)",[data,request.user.id,uploaded_file_url])
        return render(request, 'filesharing/index.html', {
            'uploaded_file_url': uploaded_file_url,
            'links':results
        })

    return render(request, 'filesharing/index.html',{'links':results})