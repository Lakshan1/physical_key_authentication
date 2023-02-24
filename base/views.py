from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


from .forms import CreateUserForm
from .models import *

# Create your views here.
@login_required(login_url="login")
def index(request):
    return render(request,"base/index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        users = Users.objects.get(user=user)

        if user is not None:
            request.session['username'] = username
            request.session['password'] = password
            if users.PKA == False:
                login(request,user)
                return redirect('index')
            else:
                request.session['unique_id'] = str(users.unique_id)
                return redirect('verification')
        else:
            return redirect('login')
        
    return render(request,'base/login.html')

def signup(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        PKA = request.POST.get('physical_key')

        if form.is_valid():
            user = form.save()

            Users.objects.create(
                user=user,
                PKA=True if PKA == "on" else False,
            )

            return redirect('login')
        else:
            return redirect('signup')

    context = {'form':form}
    return render(request,'base/signup.html',context)

def logout_view(request):
    logout(request)
    return redirect('login')

def verification(request):
    unique_id = request.session['unique_id']
    context = {'unique_id':unique_id}
    return render(request,"base/verification.html",context)

@csrf_exempt
def physical_key_authentication(request):
    if request.method == "POST":
        unique_id = request.POST.get('unique_id')
        authentication = request.POST.get('authentication')

        users = Users.objects.get(unique_id=unique_id)

        if authentication == "success": 
            users.verified = True
            users.save()
        else:
            users.verified = False
            users.save()

        return JsonResponse({'data':'success'})
    return JsonResponse({'data':'error'})

def check_authentication(request):

    user = User.objects.get(username=request.session['username'])

    users = Users.objects.get(user=user)

    print(users.verified)
    if users.verified is not None:
        if users.verified == True:
            username = request.session['username']
            password = request.session['password']  
            user = authenticate(request,username=username,password=password)
            login(request,user)

            users.verified = None
            users.save()

            return JsonResponse({'url':'http://127.0.0.1:8000/'})
        elif users.verified == False:
            users.verified = None
            users.save()
            return JsonResponse({'url':'http://127.0.0.1:8000/login/'})
    else:
        return JsonResponse({'data':'not verified yet'})