from django.urls import path,include
from django.views.generic import TemplateView
from .views import *
urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('home', home, name='home'),
    path('home/profile/', student_profile, name='profile'),
    path('apply_for_concession', student_concession, name='student_concession'),
    path('home/my_courses/', my_courses, name='my_courses'),

    path('home/scholarship_for_refugees', refugee, name='refugee'),
    path('scholarship_not_allowed/', TemplateView.as_view(template_name="schlorship_not_allowed.html"), name='scholarship_not_allowed'),
    path('scholarship_applied/', TemplateView.as_view(template_name="15_days.html"), name='scholarship_applied'),

    path('home/updateProfile/<id>', updateProfile , name='updateProfile'),
    path('upgrade_to_instructor/', upgrade_to_instructor, name='upgrade_to_instructor'),
    path('instructor_view/', instructor_mode, name='instructor_view'),
    path('courseTitle/', courseTitle, name='courseTitle'),
    path('courseTitle/courseContentCreation/<id>', courseContentCreation, name='courseContentCreation'),

    path('post/', postHomePage, name='postHomePage'),
    path('createPost/', postCreation, name='postCreation'),

    path('Courses/', Courses, name='Courses'),
    path('courseAddSection/', courseAddSection, name='courseAddSection'),


]