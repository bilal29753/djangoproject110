from django.shortcuts import render, HttpResponse,redirect,reverse
from .models import Student,Extended
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
import jwt
from  .form import MovieForm
# Create your views here.

def homepage(request):

       # return redirect(reverse('data'))
        return render(request, 'Rift_Edge.html')


def  data(request):
    students = Student.objects.all()
    return render(request, 'data.html', {'stds': students})

def formdata(request):
    if request.method == 'POST':
        name = request.POST['n']
        age = request.POST['a']
        marks = request.POST['m']
        course = request.POST['c']

        std = Student()
        std.name = name
        std.age = age
        std.marks = marks
        std.course = course

        try:
            std.save()
            return redirect(reverse('data'))
        except:
            return HttpResponse('Data not Saved')

    return HttpResponse(f'You are with Get Method')

def delete_std(request,id):
    std = Student.objects.get(pk=id)
    std.delete()

    return redirect(reverse('data'))
def update_std(request,id):
    if request.method == 'POST':
        name = request.POST['n']
        age = request.POST['a']
        marks = request.POST['m']
        course = request.POST['c']

        std = Student.objects.get(pk=id)
        std.name = name
        std.age = age
        std.marks = marks
        std.course = course

        try:
            std.save()
            return redirect(reverse('data'))
        except:
            return HttpResponse('Data not Saved')
    std = Student.objects.get(pk=id)
    return render(request, 'Form.html',{'std': std})

@login_required(login_url='/mylogin/')
def admin_panel(request):
     return render(request, 'Admin_Panel.html')



def mylogin(request):
    if request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']
        username = email.split('@')[0]

        us = authenticate(username=username, password=password)

        if us is not None:
            login(request, us)
            return redirect(reverse('admin_panel'))
        else:
            return render(request, 'Login.html',{'mes': 'wrong output'})

    if request.user.is_authenticated:
        return redirect(reverse('admin_panel'))
    else:
        return render(request, 'Login.html')

def mylogout(request):
    logout(request)
    return redirect(reverse('mylogin'))

def movie_form(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Data save..')
        else:
            return HttpResponse(f'{form.errors}')

    fmovie = MovieForm()

    return render(request, 'Form.html', {'fmovie': fmovie})

def signup(request):
    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        img = request.FILES['img']

        user = User.objects.create_user(username=username, email=email, password=password, is_active=True)
        ex = Extended()
        ex.id = user()
        ex.image = img

        ex.save()
       # enc = jwt.encode(payload={'encid': str(user.pk)}, key='secret', algorithm='HS256')
        #link = f'{request.scheme}://{request.META["HTTP_HOST"]}/activation/{enc}/'

        #em = EmailMessage('Account activation', 'Thank for creating an account\n'+link, from_email='bilaliqbal164@gmail.com', to=[email])

       # try:
        #    em.send()
        #except:
         #   HttpResponse('Unknow error occured')

        return render(request, 'Sign_Up.html', {'mes': 'Account created successfully'})
    return render(request, 'Sign_Up.html')

def activation(request, id):
    dec = jwt.decode(id, key='secret', algorithms=['HS256'])
    us = User.objects.get(pk=int(dec['encid']))
    us.is_active = True
    us.save()
    return redirect(reverse('mylogin'))

from  .models import Movie
from .serializers import MovieSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def movie_data(request):
    if request.method == 'GET':
        data = Movie.objects.all()
        sr = MovieSerializer(data, many=True)
       # return JsonResponse(sr.data, safe=False)
        return Response(sr.data)
    if request.method == 'POST':
        sr = MovieSerializer(data=request.data)
        if sr.is_valid():
            sr.save()
            data = Movie.objects.all()
            sr = MovieSerializer(data, many=True)



