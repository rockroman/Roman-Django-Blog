from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Post,Comment
from .forms import CommentForm,EmailForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
# Create your views here.


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email_form'] = EmailForm()  # Add the email form to the context
        return context

    def post(self, request, *args, **kwargs):
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipient = form.cleaned_data['recipient']
            user_email = request.user.email  # Get the email of the logged-in user

            # Send the email
            try:
                send_mail(
                    subject,
                    message,
                    user_email,  # Sender (current user's email)
                    [recipient],  # Recipient list
                    fail_silently=False,
                )
                messages.success(request, "Email sent successfully!")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")

        # Redirect or render the page with the form
        return self.get(request, *args, **kwargs)


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'commented': False,
                'liked': liked,
                'comment_form': CommentForm()
            },
            )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            messages.success(request, 'YOU ADDED A COMMENT') 
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'commented': True,
                'liked': liked,
                'comment_form': CommentForm()
            },
            )


class PostLike(View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=self.request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def delete_comment(request,comment_id,slug):
    post  = get_object_or_404(Post,slug=slug)
    comment = get_object_or_404(Comment,pk=comment_id)
    if request.user.is_authenticated:
        comment.delete()
    return redirect (reverse('home'))

        
