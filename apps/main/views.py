from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def create_user(request):
    check = User.objects.validate_user(request.POST)
    if check == True:
        user = User.objects.create(
            name = request.POST.get('name'),
            alias = request.POST.get('alias'),
            email = request.POST.get('email'),
            password = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt()),
            date_of_birth = request.POST.get('dob'),
        )
        request.session['user_id'] = user.id
        return redirect('/pokes')
    else:
        for message in check:
            messages.error(request, message)
        return redirect('/')

def login_user(request):
    login = User.objects.login_user(request.POST)
    if login[0]:
        request.session['user_id'] = login[1].id
        return redirect('/pokes')
    else:
        messages.error(request, login[1])
        return redirect('/')
    return redirect('/pokes')

def logout_user(request):
    request.session.clear()
    return redirect('/')

def main_page(request):
    pokes = User.objects.get(id = request.session['user_id'].poked.all().order_by('user.id'))
    user_ids = []
    poke_counts= []
    for poke in pokes:
        if poke.user.id not in user_ids:
            user_obj = {}
            user_obj['user'] = poke.user
            user_obj['count'] = 1
            poke_counts.append(user_obj)
            user_ids.append(poke.user.id)
        else:
            poke_counts[len(poke_counts) - 1]
    user_obj['count'] += 1

    context = {
        'pokes': pokes
    }


    # current_user = User.objects.get(id = request.session['user_id'])
    # other_user = OtherUser.objects.all()
    # poke_ids = []
    # for other_user in other_users:
    #     poke_ids.append(OtherUser.poke.id)
    # pokes = Poke.objects.exclude(id__in = poke_ids)
    # # pokes = OtherUser.pokes.all()
    # context = {
    #     'current_user': current_user,
    #     'other_user': other_user,
    #     'pokes': pokes,
    # }
    return render(request, 'main/pokes.html', context)

def poke_person(request, id):
    return redirect('/pokes')
