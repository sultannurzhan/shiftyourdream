import json
import re
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, resolve
from django.views import View
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import os
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse, HttpResponseBadRequest
from django.db import transaction
from .models import *
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

class LoginUser(View):
    def get(self, request):
        page = 'login'
        if request.user.is_authenticated:
            return redirect('home')
        context = {'page':page}
        return render(request, 'main/login_register.html', context)

    def post(self, request):
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user is None:
            messages.error(request, 'Username or Password is incorrect')
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')
            return redirect('login')

def logoutUser(request):
    logout(request)
    return redirect('default')

class RegisterUser(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'main/login_register.html')

    @csrf_exempt
    def post(self, request):
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not password1 or not password2:
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'main/login_register.html')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'main/login_register.html')

        try:
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error occurred during registration: {e}')

        return render(request, 'main/login_register.html')

class Default(View):
    def get(self, request):
        context = {}
        return render(request, 'main/default.html', context)

class Home(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        search_query = request.GET.get('q', '')
        notes = Note.objects.filter(user=request.user).filter(
            Q(title__icontains=search_query)|
            Q(body__icontains=search_query)
        ).order_by('-created')
            
        context = {'notes': notes}
        return render(request, 'main/home.html', context)
    
class Dreams(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        search_query = request.GET.get('q', '')
        sort_query = request.GET.get('sq', '')

        if sort_query == "":
            notes = Note.objects.filter(user=request.user).order_by('-created')
        elif sort_query == "Modified":
            notes = Note.objects.filter(user=request.user).order_by('-updated')
        elif sort_query == "Important":
            notes = Note.objects.filter(user=request.user, important=True).order_by('-created')

        if search_query != "":
            notes = Note.objects.filter(user=request.user).filter(
                Q(title__icontains=search_query)|
                Q(body__icontains=search_query)
            ).order_by('-created')

        context = {'notes': notes, 'sort_query': sort_query}
        return render(request, 'main/dreams.html', context)


@csrf_exempt  
def create_note(request):
    if request.method == 'POST':
        user = request.user
        title = request.POST.get('title')
        body = request.POST.get('body')
        important = request.POST.get('important') == 'true' 
        note = Note.objects.create(user=user, title=title, body=body, important=important)  
        print(request.POST.get('important'))
        note_data = {
            'id': note.id,
            'title': note.title,
            'body': note.body,
            'created': note.created,
            'updated': note.updated,
            'user_id': note.user.id,
            'important': note.important,  
        }
        return JsonResponse(note_data)
    else:
        return HttpResponseNotAllowed(['POST'])


def delete_note(request, pk):
    note = Note.objects.get(id=pk)
    if request.user != note.user:
        return redirect('home')
    if request.method == 'POST':    
        note.delete()
        return JsonResponse({'success': 'Post deleted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

def get_note_details(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    data = {
        'title': note.title,
        'body': note.body,
        'important': note.important, 
    }
    return JsonResponse(data)

def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            current_url = request.POST.get('current_url')
            return redirect(current_url)

    else:
        initial_important = note.important
        form = NoteForm(instance=note, initial={'important': initial_important})

    return render(request, 'your_template.html', {'form': form, 'note_id': note.id})


class About(View):
    def get(self, request):
        context = {}
        return render(request, 'main/about.html', context)
    
class Dashboard(View):
    def get(self, request):
        user = request.user
        my_dreams = len(Note.objects.filter(user=user))
        all_dreams = Note.objects.all()
        users = User.objects.all()
        average_dreams = len(all_dreams) / len(users)
        context = {'my_dreams': my_dreams, 'average_dreams': average_dreams}
        return render(request, 'main/dashboard.html', context)