from django.shortcuts import render
from .models import Craw
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
from .forms import NameForm
# index.html 페이지를 부르는 index 함수
def index(request):
    Craws = Craw.objects.all() 
    return render(request, 'main/index.html', {'title':'Craw List', 'Craws':Craws})
def craw(request):
	return render(request, 'main/craw.html')
def list(request):
    id = request.POST.get('userid', '')
    pw = request.POST.get('password', '')
    return render(request, 'main/list.html',{'userid': id, 'password' : pw })
