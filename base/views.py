from django.shortcuts import render, redirect
from .models import Room, Topic
from django.db.models import Q
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:

        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'WRONG USERNAME!')
        
        if user:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'WRONG PASSWORD!')


    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page ='register'
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        try:
            user_try = User.objects.get(username=username)
        except:
            if password1 == password2:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, 'Account created successfully!')
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Passwords do not match!')
        else:
            messages.error(request,'This user created!')
    
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(title__icontains=q) |
        Q(description__icontains=q) |
        Q(topic__name__icontains=q) |
        Q(host__username__icontains=q)
    )


    topics = Topic.objects.all()

    return render(request, 'base/home.html', context={'rooms': rooms, 'topics':topics})


def room(request, pk):
    room = Room.objects.get(id=pk)
    messages_room = room.message_set.all().order_by('-created')

    if request.method == 'POST':
        message = request.POST.get('message')
        room.message_set.create(body=message, user=request.user)

        room.participants.add(request.user)

        return redirect('room', pk=pk)

    return render(request, 'base/room.html',context={'room': room, 'messages_room': messages_room} )


@login_required(login_url='login-page')
def createRoom(request):
    form = RoomForm()
    
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.instance.host = request.user
            form.save()
            return redirect('home')
    
    return render(request, 'base/room_form.html', context={'form': form})


@login_required(login_url='login-page')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        messages.error(request, 'You are not the host of this room!')
        return redirect('home')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login-page')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()

        return redirect('home')
    return render(request, 'base/room_delete.html', context={'obj': room})


def profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    return render(request, 'base/profile.html', context={'user': user, 'rooms': rooms})
