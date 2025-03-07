from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from supabase import create_client

from .models import BlogPost
from .forms import PostForm

# Supabase configuration
SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_ANON_KEY = settings.SUPABASE_ANON_KEY
supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def signup_view(request):
    """Handles user signup using Supabase authentication."""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, "signup.html")

        try:
            response = supabase.auth.sign_up({"email": email, "password": password})

            if response.user:  # Check if user exists
                messages.success(request, "Signup successful! Check your email for verification.")
                return redirect("login")
            else:
                messages.error(request, "Signup failed. Try again.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return render(request, "signup.html")


def login_view(request):
    """Handles user login using Supabase authentication."""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, "login.html")

        print(f"Received email: {email}, Password: {'Yes' if password else 'No'}")  # Debugging

        try:
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})

            if response.session:  # Check if session exists
                request.session["jwt_token"] = response.session.access_token
                messages.success(request, "Login successful!")
                return redirect("blog_home")
            else:
                messages.error(request, "Invalid credentials. Please try again.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return render(request, "login.html")
def login_view(request):
    """Handles user login using Supabase authentication."""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, "login.html")

        try:
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})

            if response.session:  # Check if session exists
                request.session["jwt_token"] = response.session.access_token
                messages.success(request, "Login successful!")
                return redirect("blog_home")
            else:
                messages.error(request, "Invalid credentials. Please try again.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return render(request, "login.html")


def user_logout(request):
    """Logs out the user and redirects to the homepage."""
    request.session.flush()  # Clears session data
    messages.success(request, "Logged out successfully.")
    return redirect("blog_home")


def blog_home(request):
    """Displays all blog posts on the homepage."""
    posts = BlogPost.objects.all().order_by("-created_at")  # Ordered by latest posts
    return render(request, "blog_home.html", {"posts": posts})


@login_required
def post_detail(request, post_id):
    """Displays the details of a specific blog post."""
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, "post_detail.html", {"post": post})


@login_required
def create_post(request):
    """Allows authenticated users to create a blog post."""
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the current user as the author
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect("blog_home")
        else:
            messages.error(request, "Error creating post. Please check your input.")
    else:
        form = PostForm()
    
    return render(request, "create_post.html", {"form": form})