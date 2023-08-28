from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from notes import views
urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name='contact'),
    path('userlogin', views.userlogin, name="userlogin"),
    path('admin_login', views.admin_login, name="admin_login"),
    path('signup', views.signup1, name="signup"),
    path('admin_home', views.admin_home, name="admin_home"),
    path('logout', views.Logout, name="logout"),
    path('profile', views.profile, name="profile"),
    path('userlogout', views.userlogout, name="userlogout"),
    path('changepassword', views.changepassword, name="changepassword"),
    path('edit_profile', views.edit_profile, name="edit_profile"),
    path('upload_notes', views.upload_notes, name="upload_notes"),
    path('mynotes', views.mynotes, name="mynotes"),
    path('delete_mynotes/<int:id>', views.delete_mynotes, name="delete_mynotes"),
    path('delete_notes/<int:id>', views.delete_notes, name="delete_notes"),
    path('delete_pendingnotes/<int:id>',
         views.delete_pendingnotes, name="delete_pendingnotes"),
    path('delete_acceptednotes/<int:id>',
         views.delete_acceptednotes, name="delete_acceptednotes"),
    path('delete_rejectednotes/<int:id>',
         views.delete_rejectednotes, name="delete_rejectednotes"),
    path('view_users', views.view_users, name="view_users"),
    path('delete_user/<int:id>', views.delete_user, name="delete_user"),
    path('pending_notes', views.pending_notes, name="pending_notes"),
    path('assign_status/<int:id>', views.assign_status, name="assign_status"),
    path('accepted_notes', views.accepted_notes, name="accepted_notes"),
    path('rejected_notes', views.rejected_notes, name="rejected_notes"),
    path('all_notes', views.all_notes, name="all_notes"),
    path('change_status/<int:id>', views.change_status, name="change_status"),
    path('user_allnotes', views.user_allnotes, name="user_allnotes"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
