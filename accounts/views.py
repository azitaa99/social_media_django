from typing import Any
from django import http
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views import View
from .forms import RegisterForm, LoginForm
from .models import relation
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login ,logout, authenticate
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy




class RegisterView(View):
    form_class=RegisterForm
    def get(self, request):
        form=self.form_class()
        return render(request, 'accounts/register.html', {'form':form})

        
    def post(self, request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, 'you register successfully','success')
            return redirect('home:main_page')
        messages.error(request , 'registration field!!!', 'danger')
        return render(request, 'accounts/register.html', {'form':form})




    


class LoginView(View):
    form_class=LoginForm
    
    def setup(self, request, *args, **kwargs):
        self.next=request.GET.get('next')
        return super().setup(request, *args, **kwargs)
   
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:main_page')
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request):
        form=self.form_class()
        return render(request, 'accounts/login.html', {'form':form})
    
    def post(self, request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request,'you login seccessfully', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:main_page')
            messages.error(request, 'username or password is wrong!','danger')
        return render(request, 'accounts/login.html', {'form':form})
    

class ProfileView(LoginRequiredMixin,View):
    def get(self, request, user_id):
        is_followed=False
        user= get_object_or_404(User, pk=user_id)
        posts=user.p_user.all()
        if relation.objects.filter(from_user=request.user, to_user=user). exists():
            is_followed=True
        return render(request,'accounts/profiledetail.html', {'user':user, 'posts':posts,'is_followed':is_followed})
        
class LogoutView(LoginRequiredMixin,View):
    def get(self, request):
       logout(request)
       messages.success(request,'you logout seccessfully', 'success')
       return redirect('home:main_page')
            

class userfollowingView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user=get_object_or_404(User, id= user_id)
        Relation=relation.objects.filter(from_user=request.user, to_user=user).exists()
        if Relation:
            messages.error(request, ' you already follow this user', 'danger')
        else:
            relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request,'you follow seccessfully', 'success')
        return redirect('home:main_page')

class userunfollowingView(LoginRequiredMixin, View):
    def get(self , request, user_id):
        user=get_object_or_404(User, id=user_id)
        Relation=relation.objects.filter(from_user=request.user, to_user=user)
        if Relation.exists():
            Relation.delete()
            messages.success(request,'you unfollow seccessfully', 'success')
        else:
             messages.error(request, ' you not follow already', 'danger')
        return redirect('home:main_page')
    


# connecting google 



class userpasswordresetView(auth_views.PasswordResetView):
    template_name='accounts/pass_reset_form.html'
    success_url=reverse_lazy('accounts:pass_reset_done')
    email_template_name='accounts/pass_reset_email.html'


class userpasswordresetdoneview(auth_views.PasswordResetDoneView):
    template_name='accounts/pass_reset_done.html'


class userpasswordresetconfirmview(auth_views.PasswordResetConfirmView):
    template_name='accounts/pass_reset_confirm.html'
    success_url=reverse_lazy('accounts:pass_reset_complete')


class userpasswordresetcompleteview(auth_views.PasswordResetCompleteView):
    template_name='accounts/pass_reset_complete.html'



            









# Create your views here.
