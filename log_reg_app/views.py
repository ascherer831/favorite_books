from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    return render(request, 'reg_log.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            this_user = User.objects.create(
                first_name= request.POST['first_name'],
                last_name= request.POST['last_name'],
                email= request.POST['email'],
                password= pw_hash
            )
            request.session['user_id'] = this_user.id
            return redirect('/books')
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
        user_by_email = User.objects.filter(email=request.POST['email'])
        if user_by_email:
            this_user = user_by_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
                request.session['user_id'] = this_user.id
                return redirect('/books')
        messages.error(request, "Email or password are not valid!")
    return redirect('/')

def success(request):
    context = {
        'this_user': User.objects.get(id=request.session['user_id']),
        'all_books': Book.objects.all(),
        }
    return render(request, 'main_page.html', context)

def logout(request):
    request.session.flush()
    return redirect ('/')

# Book Methods

def create(request):
    if request.method == 'POST':
        errors = Book.objects.create_book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        else:
            this_user = User.objects.get(id=request.session['user_id'])
            this_book = Book.objects.create(
                title= request.POST['title'],
                desc= request.POST['description'],
                uploaded_by = this_user,
            )
            this_book.users_who_like.add(this_user)
            return redirect('/books')
    else:
        return redirect('/books')

def info(request,book_id):
    this_book = Book.objects.get(id=book_id)
    this_user = User.objects.get(id=request.session['user_id'])
    context = {
        'this_book': this_book,
        'this_user': this_user,
    }
    if this_book.uploaded_by.id == this_user.id:
        return render(request, 'edit.html', context)

    else:
        return render(request, 'show.html', context)

def update(request, book_id):
    update_book = Book.objects.get(id=book_id)
    errors = Book.objects.update_book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/books/{book_id}')
    else:
        update_book.title = request.POST['title']
        update_book.desc = request.POST['description']
        update_book.save()
        return redirect('/books')

def delete(request, book_id):
    this_book = Book.objects.get(id=book_id)
    this_book.delete()
    return redirect('/books')

def favorite(request, book_id):
    this_book = Book.objects.get(id=book_id)
    this_user = User.objects.get(id=request.session['user_id'])
    this_book.users_who_like.add(this_user)
    return redirect(f'/books/{book_id}')

def favorite_main(request, book_id):
    this_book = Book.objects.get(id=book_id)
    this_user = User.objects.get(id=request.session['user_id'])
    this_book.users_who_like.add(this_user)
    return redirect('/books')

def unfavorite(request, book_id):
    this_book = Book.objects.get(id=book_id)
    this_user = User.objects.get(id=request.session['user_id'])
    this_book.users_who_like.remove(this_user)
    return redirect(f'/books/{book_id}')

