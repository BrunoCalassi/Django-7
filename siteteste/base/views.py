from urllib import request
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Room, Topic
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

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:

    context = {}
    return render(request, 'base/login_register.html', context)

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
    # room= None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i 
    context = {'room': room}

    return render(request, 'base/room.html',context)

# funcao de criar rooms
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
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html', context)

# funcao deletar rooms
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})
