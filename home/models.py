from django.db import models
from django.contrib.auth.models import User





class Post(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='p_user')
    body=models.TextField()
    slug=models.SlugField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}_create_{self.slug}'
    
    def user_can_like(self, user):
        can_like=user.uvote.filter(post=self)
        if can_like.exists():
            return False
        return True






class Comment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucom')
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcom')
    body=models.TextField(max_length=400)
    reply=models.ForeignKey('comment',on_delete=models.CASCADE, blank=True, null=True, related_name='recom')
    is_reply=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-comment-{self.body[:30]}__for__{self.post.body[:30]}'
    

class Vote(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='uvote')
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pvote')

    def __str__(self):
        return f'{self.user}--like --{self.post}'
    
 

