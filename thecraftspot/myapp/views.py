from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
import razorpay
from django.conf import settings



import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Create your views here. 
def index(request):
    return render(request,'index.html')

def signup_page(request):
    return render(request, 'signup.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # Check if email already exists
        if logintable.objects.filter(email_id=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'signup.html', {'error': 'Email already exists'})

        # Save the new user
        new_user = logintable(
            username=username,
            email_id=email,
            phone_no=phone,
            password=password
        )
        new_user.save()

        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')  # After successful signup, redirect to login page
    
    return redirect('signup')

# LOGIN FORM PAGE
def login(request):
    return render(request, 'login.html')

# LOGIN FORM HANDLING
def login_check(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = logintable.objects.get(email_id=email, password=password)
            
            # Save session data
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['email'] = user.email_id
            
            messages.success(request, f"Welcome, {user.username}!")
            
            return redirect('index')  # Redirect to home page or dashboard
        
        except logintable.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return redirect('login')

# LOGOUT FUNCTION
def logout_user(request):
    request.session.flush()  # Clear all session data
    messages.success(request, "Logged out successfully!")
    return redirect('login')


def category(request):
    return render(request, 'category.html')

def about(request):
    return render(request, 'about.html')

def load_gallery_description(request):
    current_desc = request.GET.get('existing', '')

    print(current_desc)
    # print("Current description:", current_desc)  # Prints to the console
    # new_text = "This is the new description loaded from views.py!"
    if not current_desc:
        return JsonResponse({'error': 'No finding name provided'}, status=400)
    try:
        new_text = fetch_genai_description(current_desc)
        return JsonResponse({'gallery_description': new_text}, status=200)
    except Exception as e:
        return JsonResponse({'error': "At this moment no response is received from GenAI, please try again.",'details': str(e)}, status=500)
    # return JsonResponse({"gallery_description": new_text})

def fetch_genai_description(prompt):
    try:
        gemini_key = os.getenv("AIzaSyBug9bRTuSm7D9l6mWxshZuvDN8AG1KLok") or ""
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(
            [f"Tell me more about {prompt},within 2 lines"],
        )
        return response.text
        # print("GEMINI_KEY:", gemini_key)  # Debug print to see if the key is set
        # prompt += " Hello world" + gemini_key
        # return prompt
    except Exception as e:
        return str(e)


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_order(request):
    if request.method == "POST":
        amount = 50000  # Amount in paise (₹500)
        currency = "INR"
        payment_capture = 1  # Auto capture

        data = {
            "amount": amount,
            "currency": currency,
            "payment_capture": payment_capture
        }
        order = client.order.create(data)
        return JsonResponse(order)  # Returns JSON response with order details

    return render(request, "checkoutpay.html")

def checkout(request):
    print("Checkout view is being accessed")  # Debug print

    return render(request, 'checkoutpay.html')