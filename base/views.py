import json
import re
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
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
    return redirect('login')

class RegisterUser(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = RegisterUserForm()
        return render(request, 'main/login_register.html', {'form' : form})

    @csrf_exempt
    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error occured during registration')
            form = RegisterUserForm()
            return render(request, 'main/login_register.html', {'form' : form})


class Home(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        #q = request.GET.get('q') if request.GET.get('q') != None else ''
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
        important = request.POST.get('important') == 'true'  # Convert the string to a boolean
        note = Note.objects.create(user=user, title=title, body=body, important=important)  # Update Note creation
        print(request.POST.get('important'))
        note_data = {
            'id': note.id,
            'title': note.title,
            'body': note.body,
            'created': note.created,
            'updated': note.updated,
            'user_id': note.user.id,
            'important': note.important,  # Include the important field in the response
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
            home_url = reverse('home')
            return redirect(f'{home_url}#note-{note.id}')
    else:
        initial_important = note.important
        form = NoteForm(instance=note, initial={'important': initial_important})


    return render(request, 'main/home.html', {'form': form, 'note_id': note.id})