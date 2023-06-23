from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import resolve
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Topic, Room, Comment, User
from .forms import RoomForm, MyUserCreationForm, UserForm, CommentForm
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('base:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('base:home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {
        'page': page,
    }
    return render(request, 'registration/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('base:home')

def registerge(request):
    page = 'Sign Up'
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('base:home')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {
        'form': form,
        'page': page,
    }
    return render(request, 'registration/login.html', context)


def registerPage(request):
    page = 'Sign Up'
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('base:login')

    else:
        form = MyUserCreationForm()

    context = {
        'form': form,
        'page': page,
    }
    return render(request, 'registration/login.html', context)



@login_required(login_url='login')
def updateUser(request):
    page = 'User Update'

    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('base:user_profile', pk=user.id)
        else:
            messages.error(request, 'This username was already used')

    return render(request, 'registration/update-user.html', {'form': form, 'page': page,})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)                        
    )
    room_count = rooms.count()
    topics = Topic.objects.all()

    now = timezone.now()
    last = now - timezone.timedelta(minutes=30)
    comments = Comment.objects.filter(Q(room__topic__name__icontains=q)).filter(created__gte=last)

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'q': q,
        'comments': comments,
    }

    return render(request, 'home.html', context)

def room(request, pk):
    room = get_object_or_404(Room, id=pk)
    comments = room.comment_set.all().order_by('-created')
    comments_count = comments.count()
    participants = room.participants.all()
    
    if room:
        room.views = room.views + 1
        room.save()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            body = comment_form.cleaned_data['body']
            try:
                parent = comment_form.cleaned_data['parent']
            except:
                parent=None

        new_comment = Comment(body=body, user=request.user, room=room, parent=parent)
        new_comment.save()
        return redirect('base:room', pk=room.id)
    else:
        comment_form = CommentForm()

    context = {
        'room': room,
        'comment_form': comment_form,
        'comments': comments,
        'comments_count': comments_count,
        'participants': participants,
    }

    return render(request, 'room.html', context)



def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    comments = user.comment_set.all()
    topics = Topic.objects.all()
    connection = rooms.count() + comments.count()

    context = {
        'user': user,
        'rooms': rooms,
        'comments': comments,
        'topics': topics,
        'connection': connection,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='base:login')
def user_follow(request, pk):
    if request.user:
        request_user = request.user
        user = User.objects.get(id=pk)

        user.follower.add(request_user)
        user.save()

        return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'profile.html')


@login_required(login_url='base:login')
def user_unfollow(request, pk):
    if request.user:
        request_user = request.user
        user = User.objects.get(id=pk)

        user.follower.remove(request_user)
        user.save()

        return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'home.html')


@login_required(login_url='base:login')
def createRoom(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.host = request.user
            post.save()
        return redirect('base:home')
    else:
        form = RoomForm()

    topics = Topic.objects.all()
    title = 'Create'
    context = {
        'form':form,
        'title': title,
        'topics': topics,
    }

    return render(request, 'room_form.html', context)


@csrf_exempt
@login_required(login_url='base:login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    title = 'Update'

    if request.user == room.host:
        if request.method == 'POST':
            form = RoomForm(request.POST, instance=room)
            if form.is_valid():
                form.save()

                return HttpResponse("OK")
        else:return render(request, 'room_form.html', {'form':form, 'room':room, 'title':title,})  
    else:return HttpResponse('You are not allowed here')
    

@login_required(login_url='base:login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        room.delete()
        return redirect('base:home')

    context = {
        'room':room,
    }

    return render(request, 'delete_room.html', context)


def page_name(request):
    url_name = resolve(request.path).url_name
    return {'url_name': url_name}


@login_required(login_url='base:login')
def add_user_room(request, pk):
    if request.user:
        user = request.user
        room = Room.objects.get(id=pk)

        room.participants.add(user)
        room.save()

        return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'home.html')


@login_required(login_url='base:login')
def remove_user_room(request, pk):
    if request.user:
        user = request.user
        room = Room.objects.get(id=pk)

        room.participants.remove(user)
        room.save()

        return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'home.html')



@login_required(login_url='base:login')
def like_room(request, pk):
    if request.user:
        user = request.user
        room = Room.objects.get(id=pk)

        room.like.add(user)
        room.save()

        return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'home.html')


