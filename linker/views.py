from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, Http404
from .forms import UserForm, UserProfileInfoForm, LinksForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User

from .models import *

from .generate_redirect import generate_redirect_url

def index(request):
    return redirect('/linker/login/')

#Страница регистрации
def register(request):
    registered = False
    errors_user = None
    errors_profile = None
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True

            return redirect('/linker/login/')

        else:
            errors_user = user_form.errors
            errors_profile = profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'linker/register.html', {'user_form':user_form, 'profile_form':profile_form, 'registered':registered, 'errors_user':errors_user, 'errors_profile':errors_profile})


#Страница авторизации
def login_view(request):
    errors = None
    user_form = UserForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/linker/profile/{}/'.format(username))
        else:
            errors = 'Login or password is incorrect!'

    return render(request, 'linker/login.html', context={'errors':errors, 'user_form':user_form})

#Кнопка выхода
def logout_view(request):
    logout(request)
    return redirect('/linker/login/')

#Страница профиля
@login_required(login_url='/linker/login/')
def profile(request, profile_username):
    #запрет на просмотр чужих профилей
    if str(request.user) == profile_username:
        if request.user.is_authenticated:
            user = User.objects.get(username=profile_username)
            username = user.username

            links = Links.objects.filter(link_id=user)
            return render(request, 'linker/profile.html', context={'links':links, 'username':username})

            #return HttpResponse('Welcome, {}. <a href="/linker/logout/">Sign out</a>.<br><br>{}'.format(request.user, links))
        else:
            return HttpResponse('<center><b>You are not authenticated, please go to <a href="/linker/login/">login page</a>.</b></center>')
    else:
        return HttpResponse('<center><b>You can\'t to watch other profiles!</b></center>')

#добавление ссылок в базу под никами пользователей
@login_required(login_url='/linker/login/')
def add_link(request):
    reload_page = request.get_full_path()
    errors = None
    if request.method == 'POST':
        link_form = LinksForm(data=request.POST)
        if link_form.is_valid():
            user = User.objects.get(username=request.user)
            link = link_form.save(commit=False)
            link.link_redirect = generate_redirect_url()
            link.link_id, link.pub_date = user, timezone.now()

            link.save()

            return redirect(reload_page)
        else:
            errors = link_form.errors
    else:
        link_form = LinksForm()
        errors = None

    return render(request, 'linker/add_link.html', context={'link_form':link_form, 'errors':errors, 'username':request.user})

#удаление ссылок только если совпадает ник авторизиованного пользователя и ник в get-запросе!
#если попытаться поставить в адрес другого пользователя - отфутболит.
@login_required(login_url='/linker/login/')
def delete_link(request, id, profile_username):
    if str(request.user) == profile_username:
        link = Links.objects.get(pk=id)
        link.delete()
        return redirect('/linker/profile/{}/'.format(request.user))
    else:
        return HttpResponse('You cannot delete not yours link!')
    

#Вьюха для редиректов
def page_view(request, page_id):
    link_page = get_object_or_404(Links, link_redirect=page_id)
    
    get_clicks = Links.objects.get(link_redirect=page_id)
    get_clicks.clicks = int(get_clicks.clicks) + 1
    get_clicks.save()

    redirect_destination = link_page.link_source
   
    return redirect(redirect_destination)


#Установить имя пользователя
@login_required(login_url='/linker/login/')
def settings_view(request):
    reload_page = request.get_full_path()
    if request.method == 'POST':
        user = User.objects.get(username=str(request.user))
        update_data = UserProfileInfo.objects.get(user=user)

        user.email = request.POST['email']
        user.username = request.POST['username']
        user.save()

        update_data.firstname = request.POST['firstname']
        update_data.lastname = request.POST['lastname']
        update_data.save()

        return redirect(reload_page)
    
    else:
        username = request.user
        user = User.objects.get(username=username)
        data = UserProfileInfo.objects.get(user=user)

        user_form = UserForm(data={'username':user.username, 'email':user.email})
        profile_form = UserProfileInfoForm(data={'firstname':data.firstname, 'lastname':data.lastname})

        return render(request, 'linker/settings.html', context={'username':username, 'user_data':user, 'profile_data':data, 'profile_form':profile_form, 'user_form':user_form})