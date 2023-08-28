from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from notes import models
from django.contrib.auth.models import User
from datetime import date

# Create your views here.


def index(request):
    return render(request, 'notes/index.html')


def about(request):
    return render(request, 'notes/about.html')


def contact(request):
    return render(request, 'notes/contact.html')


def userlogin(request):
    error = ""
    if request.method == "POST":
        e = request.POST['emailid']
        p = request.POST['password']
        user = authenticate(username=e, password=p)
        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    context = {
        "error": error
    }
    return render(request, 'notes/login.html', context)


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"

        except:
            error = "yes"

    context = {"error": error}

    return render(request, 'notes/admin_login.html', context)


def signup1(request):
    error = ""
    if request.method == "POST":
        f = request.POST['firstname']
        l = request.POST['lastname']
        c = request.POST['contact']
        e = request.POST['email']
        p = request.POST['password']
        b = request.POST['branch']
        r = request.POST['role']
        try:
            user = User.objects.create_user(
                username=e, password=p, first_name=f, last_name=l)
            models.signup.objects.create(
                user=user, contact=c, branch=b, role=r)
            error = "no"
        except:
            error = "yes"
    context = {
        "error": error
    }
    return render(request, 'notes/signup.html', context)


def admin_home(request):
    # if not request.user.is_staff:
    #     return redirect('admin_login')
    pending = models.Notes.objects.filter(status="pending").count()
    accepted = models.Notes.objects.filter(status="accepted").count()
    rejected = models.Notes.objects.filter(status="rejected").count()
    all = models.Notes.objects.all().count()
    data = {
        "accepted": accepted,
        "rejected": rejected,
        "pending": pending,
        "all": all,
    }
    return render(request, 'notes/admin_home.html', data)


def Logout(request):
    logout(request)
    return redirect('admin_login')


def userlogout(request):
    logout(request)
    return redirect('userlogin')


def profile(request):
    user = User.objects.get(id=request.user.id)
    data = models.signup.objects.get(user=user)
    context = {
        "user": user,
        "data": data,
    }
    return render(request, 'notes/profile.html', context)


def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')

    error = ""
    if request.method == "POST":
        oldpwd = request.POST['oldpwd']
        newpwd = request.POST['newpwd']
        confirm = request.POST['confirm']

        if newpwd == confirm:
            u = User.objects.get(username=request.user.username)
            u.set_password(newpwd)
            u.save()
            error = "no"
        else:
            error = "yes"

    context = {
        "error": error
    }
    return render(request, 'notes/changepassword.html', context)


def edit_profile(request):
    user = User.objects.get(id=request.user.id)
    data = models.signup.objects.get(user=user)
    context = {
        "user": user,
        "data": data,
    }
    error = True
    if request.method == "POST":
        f = request.POST['firstname']
        l = request.POST['lastname']
        c = request.POST['contact']
        b = request.POST['branch']
        r = request.POST['role']
        user.first_name = f
        user.last_name = l
        data.contact = c
        data.branch = b
        data.role = r
        user.save()
        data.save()
        error = False
    context = {
        "user": user,
        "data": data,
        "error": error,
    }
    return render(request, 'notes/edit_profile.html', context)


def upload_notes(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    error = ""
    if request.method == "POST":
        b = request.POST['branch']
        s = request.POST['subject']
        n = request.FILES['notesfile']
        f = request.POST['filetype']
        d = request.POST['description']
        u = User.objects.filter(username=request.user.username).first()
        try:
            models.Notes.objects.create(user=u, branch=b, subject=s,
                                        notes_file=n, filetype=f, description=d, uploading_date=date.today())
            error = "no"
        except:
            error = "yes"
    context = {
        "error": error
    }
    return render(request, 'notes/upload_notes.html', context)


def mynotes(request):
    user = User.objects.get(id=request.user.id)
    notes = models.Notes.objects.filter(user=user)
    data = {
        "notes": notes
    }
    return render(request, 'notes/mynotes.html', data)


def user_allnotes(request):
    notes = models.Notes.objects.all()
    data = {
        "notes": notes
    }
    return render(request, 'notes/user_allnotes.html', data)


def delete_mynotes(request, id):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    notes = models.Notes.objects.get(id=id)
    notes.delete()
    return redirect('mynotes')


def delete_acceptednotes(request, id):
    if not request.user.is_staff:
        return redirect('userlogin')
    notes = models.Notes.objects.get(id=id)
    notes.delete()
    return redirect('accepted_notes')


def delete_rejectednotes(request, id):
    if not request.user.is_staff:
        return redirect('userlogin')
    notes = models.Notes.objects.get(id=id)
    notes.delete()
    return redirect('rejected_notes')


def delete_pendingnotes(request, id):
    if not request.user.is_staff:
        return redirect('userlogin')
    notes = models.Notes.objects.get(id=id)
    notes.delete()
    return redirect('pending_notes')


def delete_notes(request, id):
    if not request.user.is_staff:
        return redirect('userlogin')
    notes = models.Notes.objects.get(id=id)
    notes.delete()
    return redirect('all_notes')


def view_users(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    users = models.signup.objects.all()
    data = {
        "users": users
    }
    return render(request, 'notes/view_users.html', data)


def delete_user(request, id):
    if not request.user.is_staff:
        return redirect('admin_login')

    user = User.objects.get(id=id)
    user.delete()
    return redirect('view_users')


def pending_notes(request):
    notes = models.Notes.objects.filter(status="pending")
    data = {
        "notes": notes
    }
    return render(request, 'notes/pending_notes.html', data)


def assign_status(request, id):
    error = ""
    notes = models.Notes.objects.get(id=id)
    if request.method == "POST":
        try:
            st = request.POST['status']
            notes.status = st
            notes.save()
            error = "no"
        except:
            error = "yes"
    context = {
        "notes": notes,
        "error": error
    }
    return render(request, 'notes/assign_status.html', context)


def accepted_notes(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    notes = models.Notes.objects.filter(status="accepted")
    data = {
        "notes": notes
    }
    return render(request, 'notes/accepted_notes.html', data)


def rejected_notes(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    notes = models.Notes.objects.filter(status="rejected")
    data = {
        "notes": notes
    }
    return render(request, 'notes/rejected_notes.html', data)


def all_notes(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    notes = models.Notes.objects.all()
    data = {
        "notes": notes
    }
    return render(request, 'notes/all_notes.html', data)


def change_status(request, id):
    notes = models.Notes.objects.get(id=id)
    if notes.status == "accepted":
        notes.status = "rejected"
        notes.save()
        return redirect('accepted_notes')
    else:
        notes.status = "accepted"
        notes.save()
        return redirect('rejected_notes')
