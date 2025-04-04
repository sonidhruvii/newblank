from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Sum
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
import razorpay
from django.conf import settings
from .models import Category,login,product,cartable,contact_us,order
from django.contrib.auth.hashers import check_password
import logging


import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Create your views here. 
def index(request):
    fetchcatdata = Category.objects.all()
    context = {

        "catdata": fetchcatdata
    }
    return render(request,'index.html',context)

def registerpage(request):
    return render(request, "register.html")
    
    fetchregdata = login.objects.all()
    fetchcatdata = Category.objects.all()
    print(fetchregdata)

    context = {
        "data":fetchregdata,
         "catdata": fetchcatdata
    }
    return render(request, "register.html",context)

def loginpage(request):

    fetchcatdata = Category.objects.all()
    context = {
        "catdata": fetchcatdata
    }
    return render(request,"login.html")
#     # return render(request,"login.html")
def insertregisterdata(request):
    fetchcatdata = Category.objects.all()

    context = {
        "catdata": fetchcatdata
    }
    if request.method == "POST":
        uname = request.POST.get("username")
        uemail = request.POST.get("useremail")
        uphone = request.POST.get("userphone")
        upass = request.POST.get("userpassword")
       
        uaddress = request.POST.get("address")
        ugender = request.POST.get("usergender")
        
        ustatus = request.POST.get("userstatus",default='active')
        vquery =login.objects.filter(EMAIL_ID=uemail)
        if vquery.exists():
            messages.error(request,"Email Already Exist")
            return render(request,'register.html',context)
        else:
            insertdata = login(U_NAME=uname,EMAIL_ID=uemail,PASSWORD=upass,PHONE_NO=uphone,U_ADDRESS=uaddress,U_GENDER=ugender,STATUS=ustatus)
            # ,ROLE_TYPE=urole
            insertdata.save()
            # return render(request,"index.html")
            messages.success(request,'Registered Succesfully ')
            # return redirect(loginpage)
            return render(request, "login.html")
    else:
        messages.error(request, "Unable to Register")
        return render(request, 'register.html',context)


# def insertproductdata(request):

def checklogindata(request):
    fetchcatdata = Category.objects.all()

    context = {
        "catdata": fetchcatdata
    }

    # uname = request.POST.get("username")
    uemail = request.POST.get("useremail")
    upass = request.POST.get("userpassword")

    try:
        checkuser = login.objects.get(EMAIL_ID=uemail,PASSWORD=upass)

        request.session["logid"] = checkuser.id
        request.session["logname"] = checkuser.U_NAME
        request.session.save()

    except:
        checkuser = None

    if checkuser is not None:
        return redirect("/")

    else:
        print("incorrect details")
        messages.error(request,"Invalid Email or Password.Please try again")
        # print(uname)
        # print(uemail)
        # print(upass)

    return render(request,"login.html",context)
# LOGOUT FUNCTION
def logout(request):
    fetchcatdata = Category.objects.all()
    context = {
        "catdata": fetchcatdata
    }
    try:
        del request.session["logid"]
        del request.session["logname"]
    except:
        pass
    messages.success(request, "Logged Out Successfully")
    return render(request,"login.html",context)

# def category(request):
#     return render(request, 'category.html')
def discoverpage(request):
    fetchcatdata = Category.objects.all()
    print(fetchcatdata)
    context = {
        "data": fetchcatdata,

    }
    return render(request, "discover.html", context)


def addproduct(request):
    allcat = Category.objects.all()
    context ={
        'allcat':allcat
    }
    return render(request,'productfilter.html',context)

def showprofile(request):
    uid = request.session["logid"]
    fetchuserdata =login.objects.get(id=uid)
    fetchcatdata = Category.objects.all()
    context ={
        "userdata": fetchuserdata,
        "catdata": fetchcatdata
    }
    return render(request,"showprofile.html",context)

def editprofile(request):
    uid = request.session["logid"]
    getdata = login.objects.get(id=uid)
    context ={
        "data":getdata
    }
    return render(request,"editprofile.html",context)
def showorders(request):
    uid = request.session["logid"]
    fetchorderdata = order.objects.filter(LOGIN_ID=uid)
    fetchcatdata = Category.objects.all()
    context = {
        "orderdata":fetchorderdata,
        "catdata": fetchcatdata
    }
    return render(request,"showorders.html",context)

def updateprofile(request):
    uid = request.POST.get("loginid")
    uname = request.POST.get("username")
    uemail = request.POST.get("useremail")
    uphone = request.POST.get("userphone")
    uaddress = request.POST.get("address")
    ugender = request.POST.get("usergender")

    getdata = login.objects.get(id=uid)
    getdata.U_NAME =uname
    getdata.EMAIL_ID =uemail
    getdata.PHONE_NO =uphone
    getdata.U_ADDRESS =uaddress
    getdata.U_GENDER=ugender
    getdata.save()
    return redirect("/profile")

def addproductdetails(request):
    try:
        if request.method == 'POST':
            pro_name = request.POST.get("Product Name")
            pro_category = request.POST.get("Product Category")
            pro_img = request.FILES["Product Image"]
            pro_desc = request.POST.get("Product Description")
            pro_price = request.POST.get("Product Price")

            pro = product(ITEM_NAME=pro_name, CAT_ID=Category(id=pro_category),ITEM_IMG=pro_img, ITEM_DESC=pro_desc, ITEM_PRICE=pro_price)
            pro.save()
        messages.success(request,'Product added')
        return redirect(index)
    except Exception as e:
        print("error\n",e)
        return redirect(loginpage)


def about(request):
    return render(request, 'about.html')

def catproductpage(request , cid):
    fetchproductdata = product.objects.filter(CAT_ID=cid)
    fetchcatdata = Category.objects.all()

    print(fetchproductdata)
    context = {
        "data": fetchproductdata,
        "catdata":fetchcatdata
    }
    return render(request, "productfilter.html",context)

def shopsinglepage(request, pid):
    # return render(request, "shop-single.html")
    fetchcatdata = Category.objects.all()

    getsingledata = product.objects.get(id=pid)
    context= {
        "data" : getsingledata,
        "catdata": fetchcatdata
    }

    return render(request, "shop-single.html",context)
def addtocart(request):
    uid = request.session["logid"]
    quantity = request.POST.get("quantity")
    prodid = request.POST.get("pid")
    proprice = request.POST.get("price")
    proprice = float(proprice)
    # quantity = int(quantity)
    quantity = float(quantity)
    totalamount = proprice * quantity

    try:
        checkitemincart = cartable.objects.get(LOGIN_ID=uid,PROD_ID=prodid,Cart_STATUS=1)
    except:
        checkitemincart =None

    if checkitemincart is None:

        storedata =cartable(LOGIN_ID=login(id=uid),PROD_ID=product(id=prodid),QUANTITY=int(quantity),Totalamount=totalamount,Cart_STATUS=1,ORDER_ID=0)

        storedata.save()
        messages.success(request,"product added to cart")
    else:
        checkitemincart.QUANTITY += quantity
        checkitemincart.Totalamount += totalamount
        checkitemincart.save()

    # return redirect("/index")
    # return render(request,"shop.html")
    return redirect("/shop")

def shoppage(request):
    fetchproductdata = product.objects.all()
    fetchcatdata = Category.objects.all()
    print(fetchproductdata)
    context = {
        "data": fetchproductdata,
        "catdata":fetchcatdata
    }


    return render(request, "shop.html", context)

def shoppingcartpage(request):
    uid = request.session["logid"]
    fetchcatdata = Category.objects.all()
    fetchcartdata = cartable.objects.filter(LOGIN_ID=uid, Cart_STATUS=1)

    # Calculate the total amount without shipping charge
    order_total = fetchcartdata.aggregate(total=Sum('Totalamount'))['total']

    # Add flat shipping charge of 100 rupees
    shipping_charge = 100

    # Add shipping charge to the total amount
    final_total = order_total + shipping_charge if order_total is not None else shipping_charge

    context = {
        "cartdata": fetchcartdata,
        "catdata": fetchcatdata,
        "finaltotal": final_total
    }
    return render(request, "shopping-cart.html", context)

def fetchorderdetails(request):
    uid = request.session["logid"]
    name =request.POST.get("uname")
    address =request.POST.get("address")
    finaltotal =request.POST.get("total")
    payment =request.POST.get("payment-group")

    insertdata = order(LOGIN_ID=uid, FINALTOTAL=finaltotal, PAY_MODE=payment, NAME=name, ADDRESS=address)
    insertdata.save()

    last_inserted_id = insertdata.id
    print(last_inserted_id)

    fetchcartdata = cartable.objects.filter(LOGIN_ID=uid, Cart_STATUS=1)
    fetchcatdata = Category.objects.all()
    context = {

        "catdata": fetchcatdata
    }
    for i in fetchcartdata:
        i.ORDER_ID = last_inserted_id
        i.Cart_STATUS = 2
        i.save()

    # messages.success(request,"Order place successfully")
    messages.success(request, 'Order Place Successfully')
    return redirect('/',oid=last_inserted_id)

def showorders(request):
    orders = order.objects.all()  # Fetch all orders
    return render(request, "showorders.html", {"orders": orders})

def viewsingleorder(request , id):
    fetchsingleorder = cartable.objects.filter(ORDER_ID=id)
    fetchcatdata = Category.objects.all()
    context = {
        "data":fetchsingleorder,
        "catdata": fetchcatdata
    }
    return render(request,"singleorder.html",context)


logger = logging.getLogger(__name__)

def order_success(request):
    logger.info(f"Request Method: {request.method}")

    # -------------------------------
    # Handle GET (Online Payment Success Page Load)
    # -------------------------------
    if request.method == "GET":
        payment_id = request.GET.get("payment_id")
        order_id = request.GET.get("order_id")

        if order_id:
            # COD Order - from form submission redirect
            user_order = get_object_or_404(order, id=order_id)
            return render(request, "order_success.html", {"order": user_order})

        elif payment_id:
            # Razorpay success redirect - optional, for frontend use only
            return render(request, "order_success.html", {"payment_id": payment_id})

        return render(request, "order_success.html", {"error": "Invalid or missing order ID."})

    # -------------------------------
    # Handle POST (COD or Razorpay)
    # -------------------------------
    if request.method == "POST":
        logger.info(f"POST Data: {request.POST}")

        user_id = request.POST.get("user_id")
        name = request.POST.get("uname")
        final_total = request.POST.get("total", "0")
        address = request.POST.get("address")
        pay_mode = request.POST.get("payment-group")
        payment_id = request.POST.get("payment_id", None)

        if not all([user_id, name, final_total, address, pay_mode]):
            logger.error("Missing form data")
            return JsonResponse({"success": False, "error": "Missing form data"}, status=400)

        user = login.objects.filter(id=user_id).first()
        if not user:
            logger.error("User not found")
            return JsonResponse({"success": False, "error": "User not found"}, status=400)

        # Save the order
        new_order = order.objects.create(
            LOGIN_ID=user,
            NAME=name,
            FINALTOTAL=final_total,
            ADDRESS=address,
            PAY_MODE=pay_mode,
            PAYMENT_ID=payment_id
        )

        logger.info(f"Order created successfully! ID: {new_order.id}")

        # Respond with JSON to be used in JS
        return JsonResponse({
            "success": True,
            "redirect_url": f"/order-success?order_id={new_order.id}"
        })

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


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

def checkout(request,id):
    fetchcatdata = Category.objects.all()
    context = {
        "total":id,
        "catdata": fetchcatdata
    }

    print("Checkout view is being accessed")  # Debug print

    return render(request, 'checkoutpay.html',context)


def contactpage(request):
    fetchcontactdata = contact_us.objects.all()
    fetchcatdata = Category.objects.all()
    print(fetchcontactdata)
    context = {
        "data" : fetchcontactdata,
        "catdata": fetchcatdata
    }
    return render(request, "contact.html",context)
    # return render(request, "contact.html")



def insertcontactdata(request):
    sub = request.POST.get("subject")
    uname = request.POST.get("username")
    uemail = request.POST.get("email")
    uphone = request.POST.get("phone")
    msg = request.POST.get("message")

    insertcontdata = contact_us(Subject=sub,U_NAME=uname,Email_ID=uemail,Phone_NO=uphone,MESSAGE=msg)
    insertcontdata.save()
    

            # return redirect(loginpage)
    return render(request, "contact.html")

def increaseitem(request, id):
    getitemdetail =cartable.objects.get(id=id)
    getitemdetail.QUANTITY  += 1
    getitemdetail.Totalamount += getitemdetail.PROD_ID.ITEM_PRICE
    getitemdetail.save()
    return redirect("/shopping-cart")
def decreaseitem(request,id):
    getitemdetail =cartable.objects.get(id=id)
    QUANTITY = getitemdetail.QUANTITY

    if QUANTITY==1:
        getitemdetail.delete()
        return redirect("/shopping-cart")
    else:
        getitemdetail.QUANTITY -= 1
        getitemdetail.Totalamount -= getitemdetail.PROD_ID.ITEM_PRICE
        getitemdetail.save()
        return redirect("/shopping-cart")
    
def removeitem(request,id):
    fetchitemfromcart = cartable.objects.get(id=id)
    # fetchitemfromcart.delete()
    # fetchitemfromcart.save()
    fetchitemfromcart.Cart_STATUS =0
    fetchitemfromcart.save()
    return redirect("/shopping-cart")