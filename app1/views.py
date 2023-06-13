from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseForbidden

def all_login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        if not request.POST.get('remember_me',None): #remember me
            request.session.set_expiry(0)
        user=authenticate(username=username,password=password)
        if user is not None:
            request.session['user']=user.username # remember me
            login(request,user)
            if user.role == 1 :
                return redirect ('admin_home')
            elif user.role == 2 :
                return redirect ('user_home')
        else:
            return redirect ('/')
    return render (request,'login.html')


def logoutall(request):
    logout(request)
    return redirect ('/')

def user_register(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        course=request.POST.get('course')
        
        if password1==password2:
            user=CustomUser.objects.create_user(
                username=username,
                password=password1,
                email=email,
                role=2, 
            )
            UserProfile.objects.create(
                fk_user=user,
                firstname=firstname,
                lastname=lastname,
                course=course,
                user_status=False,
            )
            return redirect ('all_login')
        else:
            messages.error(request,'incorrect password')
    return render(request,'register.html')

def user_home(request):
    user=UserProfile.objects.get(fk_user=request.user)
    results=Result.objects.filter(fk_user=request.user)
   
    if not user.user_status:          
         return HttpResponseForbidden("Your account is not yet approved by the admin.")
    
    userdetails=UserProfile.objects.filter(fk_user=request.user)

    context={
        'user':userdetails,
        'results':results,
    }
    return render(request,'user_home.html',context)

def admin_home(request):
    users=UserProfile.objects.all()
    tasks=Task.objects.all()
    results=Result.objects.all().order_by('-id')
    context={
        'users':users,
        'tasks':tasks,
        'results':results,
    }
    return render(request,'admin_home.html',context)

def admin_approve(request):
    if request.method == 'POST':
        user_id=request.POST.get('approve')
        user=UserProfile.objects.get(id=user_id)
        user.user_status = True
        user.save()
        return redirect ('admin_home')
    unapproved= UserProfile.objects.filter(user_status=False)
    context={ 
        'unapproved':unapproved
    }
    return render(request,'approve.html',context) 

def add_task(request):
    if request.method == 'POST':
        question=request.POST.get('question')
        option1=request.POST.get('option1')
        option2=request.POST.get('option2')
        option3=request.POST.get('option3')
        option4=request.POST.get('option4')
        answer=request.POST.get('answer')
        Task.objects.create(
            question=question,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            answer=answer
        )
        return redirect('admin_home')
    return render(request,'add_task.html') 

def edit_task(request,id):
    task=Task.objects.get(id=id)
    if request.method == 'POST':
        question=request.POST.get('question')
        option1=request.POST.get('option1')
        option2=request.POST.get('option2')
        option3=request.POST.get('option3')
        option4=request.POST.get('option4')
        answer=request.POST.get('answer')
        if question:
            task.question=question
        if option1:
            task.option1=option1
        if option2:
            task.option2=option2
        if option3:
            task.option3=option3
        if option4:
            task.option4=option4
        if answer:
            task.answer=answer
        task.save()
        return redirect ('admin_home')
    return render (request,'edit_task.html',{'task':task})

def delete_task(request,id):
    task=Task.objects.get(id=id)
    task.delete()
    return redirect ('admin_home')

def test(request):
    user=request.user
    tasks=Task.objects.all()
    mark=0
    count=0
    if request.method == 'POST':
        for task in tasks:
            answer=request.POST.get(f'answer_{task.id}')
            Exam.objects.create(
                answer=answer,
                fk_user=user,
                fk_task=task,
            )
            if answer == task.answer:
                mark += 1.0
                count +=1.0
            else:
                if answer is None:
                    mark += 0
                    count += 1.0
                else:
                    mark -= 0.25
                    count +=1.0
        Result.objects.create(
            fk_user=user,
            mark=mark,
            total=count,
        )
        return redirect('complete', mark=str(mark),count=str(count))
    return render (request,"test.html",{'tasks':tasks})
    
def complete(request,mark,count):
    user=UserProfile.objects.get(fk_user=request.user)
    context = {'mark':mark,'count':count,'user':user}
    return render(request, 'complete.html',context)