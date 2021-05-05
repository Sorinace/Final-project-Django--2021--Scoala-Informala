import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def admin(request):
    time = datetime.datetime.now()
    return render(request, 'about.html',{'time': time})