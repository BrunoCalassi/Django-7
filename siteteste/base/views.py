from email import message
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
# query de pesquisa com OR e AND
from .forms import RoomForm
# Create your views here.

# rooms =[
#     {'id': 1 , 'name': 'Exemplo 1'},
#     {'id': 2 , 'name': 'Exemplo 2'},
#     {'id': 3 , 'name': 'Exemplo 3'},
# ]

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
            messages.error(request, 'User nao encontrado.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User ou senha nao encontrado.')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'Erro no cadastro')


    return render(request, 'base/login_register.html', {'form': form})

# Da pagina principal
def home(request):
    # pega o valor do search 
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    # contains é case sensitive, filtro com ou |   and é &
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
    )
    topics = Topic.objects.all() #pega os topicos
    room_count = rooms.count()#conta as salas
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)

# funcao de ver rooms
def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    # room= None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i 
    participants = room.participants.all()
    if request.method =='POST':
        message = Message.objects.create(
            user = request.user,
            room=room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room , 'room_messages':room_messages, 'participants':participants}

    return render(request, 'base/room.html',context)

# funcao de criar rooms
@login_required(login_url='login') # precisa de login para usar essa funcao, redireciona para a pagina de login
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html', context)

# funcao dar update rooms
@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Usuario diferente')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html', context)

# funcao deletar rooms
@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Usuario diferente')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Usuario diferente')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})
