from django.http import request
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/main_page')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/main_page')

def main_page(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'all_quotes': Quote.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id'])
        }
    return render(request, 'main_page.html', context)

def user_account(request, id):
    if "user_id" not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'edit_account.html', context)

def edit_user(request, id):
    if "user_id" not in request.session:
        return redirect('/')
    errors = User.objects.update_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/user_account/{id}")
    else:
        edit_user = User.objects.get(id=id)
        edit_user.first_name = request.POST['first_name']
        edit_user.last_name = request.POST['last_name']
        edit_user.email = request.POST['email']
        edit_user.save()
        return redirect('/main_page')
    
def user_quote(request, id):
    if "user_id" not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'profile.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def submit_quote(request):
    if "user_id" not in request.session:
        return redirect('/')
    errors = User.objects.quote_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/main_page')
    else:
        user_quote = User.objects.get(id=request.session['user_id'])
        Quote.objects.create(quote_author=request.POST['quote_author'], quote=request.POST['quote'], user_quote=User.objects.get(id=request.session['user_id']))
        return redirect('/main_page')

def delete_quote(request, id):
    if "user_id" not in request.session:
        return redirect('/')
    destroyed = Quote.objects.get(id=id)
    destroyed.delete()
    return redirect('/main_page')
    
def add_like(request, id):
    if "user_id" not in request.session:
        return redirect('/')
    liked_quote = Quote.objects.get(id=id)
    like_activity = User.objects.get(id=request.session['user_id'])
    liked_quote.likes.add(like_activity)
    return redirect('/main_page')

