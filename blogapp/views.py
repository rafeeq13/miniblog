from django.shortcuts import render,HttpResponseRedirect
from .forms import Signup,Login_form,Postform
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group

# Create your views here.
def home(request):
    post=Post.objects.all()
    return render(request,'enroll/home.html',{'posts':post})

#about Page  
def about(request):
    return render(request,'enroll/about.html')

#contact form
def contact(request):
    return render(request,'enroll/contact.html')

#dashboard
def dashboard(request):
    if request.user.is_authenticated:
        fm=Post.objects.all()
        user=request.user
        full_name=user.get_full_name()
        gps=user.groups.all()
        return render(request,'enroll/dashboard.html',{'form':fm,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')
#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#signup form
def user_signup(request):
    if request.method=="POST":
        fm=Signup(request.POST)
        if fm.is_valid():
            messages.info(request,'Congrates you have been a new User')
            user=fm.save()
            group=Group.objects.get(name="Author")
            user.groups.add(group)
    else:
        fm=Signup()
    return render(request,'enroll/signup.html',{'form':fm})
#log in form
def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            fm=Login_form(request=request,data=request.POST)
            if fm.is_valid():
                nm=fm.cleaned_data['username']
                pwd=fm.cleaned_data['password']
                user=authenticate(username=nm,password=pwd)
                if user is not None:
                    login(request,user)
                    messages.success(request,'You"ve loged in successfully')
                    return HttpResponseRedirect('/dashboard/')
        fm=Login_form()
        return render(request,'enroll/login.html',{'form':fm})
    else:
        return HttpResponseRedirect('/dashboard/')
#add POst
def addpost(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            fm=Postform(request.POST)
            if fm.is_valid():
                messages.success(request,'your post added successfull')
                fm.save()
                fm=Postform()
        else:
            fm=Postform()
        return render(request,'enroll/addpost.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')

#update post
def updatepost(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=Post.objects.get(pk=id)
            fm=Postform(request.POST, instance=pi)
            if fm.is_valid():
                fm.save()

        else:
            pi=Post.objects.get(pk=id)
            fm=Postform(request.POST,instance=pi)           
        return render(request,'enroll/update.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')

#delete Post 
def deletepost(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')