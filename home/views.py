from typing import Any
from django import http
from django.http.response import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404,get_list_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm, updatepostForm, CommentForm, ReplyForm, postserachForm
from .models import Post , Comment, Vote
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator





class mainpageView(View):
    form_class=postserachForm
    def get(self , request):
        posts=get_list_or_404(Post)
        if request.GET.get('search'):
            posts=Post.objects.filter(body__contains=request.GET['search'])
        return render(request, 'home/mainpage.html', {'posts':posts, 'form':self.form_class} )
    

class CreatpostView(LoginRequiredMixin, View):
    form_class= PostForm
    template_url='home/createpost.html'

    def get(self, request):
        return render(request,self.template_url,{'form':self.form_class})
    def post(self, request):
        form=self.form_class(request.POST)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.user=request.user
            new_post.slug=slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'new post created','success')
            return redirect('home:main_page')
        messages.error(request, 'creating new post faild!','danger')
        return render(request,self.template_url, {'form':self.form_class,} )
    
class PostdetailView(View):
    form_class=CommentForm
    form_class_reply=ReplyForm
    def setup(self, request, *args: Any, **kwargs: Any):
        self.post_instance=Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)
    
    def get(self,request, *args, **kwargs):
        form=self.form_class
        comments=self.post_instance.pcom.filter(is_reply=False)
        can_like=False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like=True
        return render(request, 'home/postdetail.html', {'post':self.post_instance, 'comments':comments, 'form' : form, 'replyform':self.form_class_reply, 'can_like':can_like})
    
    @method_decorator(login_required)
    def post(self, request,*args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.user=request.user
            new_comment.post=self.post_instance
            new_comment.save()
            messages.success(request, 'you commented successfully','success')
            return redirect('home:post_detail', self.post_instance.id)
        messages.error(request,'faild', 'danger')
        return redirect('home:post_detail', self.post_instance.id)
    
class replycommentView(LoginRequiredMixin,View):
    form_class=ReplyForm
    def post(self,request, post_id, comment_id):
        post=get_object_or_404(Post,pk=post_id)
        Commentt=Comment.objects.get(pk=comment_id)
        form=self.form_class(request.POST)
        if form.is_valid():
            reply=form.save(commit=False)
            reply.user=request.user
            reply.post=post
            reply.reply=Commentt
            reply.is_reply=True
            reply.save()
            messages.success(request,'rply send sucessfully', 'success')
        return redirect('home:post_detail', post.id)


    


class updatepostView(LoginRequiredMixin, View):
    form_class=updatepostForm
    def setup(self, request, *args, **kwargs):
        self.post_instance=get_object_or_404(Post, id=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, ' you cant update this post', 'danger')
            return redirect('home:main_page')
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request, post_id):
        post=self.post_instance
        form=self.form_class(instance=post)
        return render(request, 'home/updatepost.html', {'form':form})

    def post(self, request, post_id):
        post=self.post_instance
        form=self.form_class(request.POST, instance=post)
        if form.is_valid():
            up_post=form.save(commit=False)
            up_post.slug=slugify(form.cleaned_data['body'][:30])
            up_post.save()
            messages.success(request, ' post  update sucessfully','success')
            return redirect('home:post_detail' , post.id)
        messages.error(request, 'update post faild!','danger')
        return redirect('home:post_detail', post.id)


class deletpostView(LoginRequiredMixin,View):
    def get(self,request, post_id):
        post=Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request,'post remove successfully', 'sucess')
        else:
            messages.error(request,'faild!', 'danger')
        return redirect('home:main_page')

    
class postlikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post=get_object_or_404(Post, pk=post_id)
        like=Vote.objects.filter(user=request.user, post=post)
        if like.exists():
            messages.error(request,'you liked this post already!', 'danger')
        else:
            Vote.objects.create(user=request.user, post=post)
            messages.success(request,'post liked successfully', 'sucess')
        return redirect('home:post_detail', post.id)




        

# Create your views here.
