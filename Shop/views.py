from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, request
from django.contrib.auth import logout,login,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
import json
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
from django.views.generic.base import TemplateView
stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

def Home(request):
   user = User.objects.all() 
   return render(request,'index.html')


#######################Signup###################


class Register(View):
    # template_name="register.html"
    def get(self,request):
        print("in get method")
        return render(request,'register.html')


    def post(self,request):
        # print(request.POST,'---rrrppppp')
        print("in post method")
        
        # {
        #     'status' : False
        # }
        
        username= request.POST.get('username')
        password=request.POST.get('password')
        confirmpass=request.POST.get('repeatpassword')
        email= request.POST.get('email')

        print(request.POST)

        

        try:
            User.objects.get(email=email)
            return HttpResponse("email already exists")

        except User.DoesNotExist:
            if password == confirmpass:
                u=User.objects.create(username=username,email=email)
                u.set_password(password)
                u.save()
                # data['status'] = True
                # data['message'] = 'updated!'
                messages.success(request, 'Now you can login')
                return HttpResponseRedirect('login')
                # return HttpResponse("REGISTERRRRR")
            else:
                messages.error(request, 'password doesnt match')
                return HttpResponse("password doesnot match")
        except Exception as e:
            print(e)
            return HttpResponse("facing exception")
            # data['status'] = False
            # data['message'] = 'Error'
        # finally:
        #     return HttpResponse(json.dumps(data), content_type="application/json")







#########################Login#############################

class Login(View):
    def get(self,request):
        print("in get method")
      
        return render(request,'login.html')
    def post(self,request):
        
        print(request.POST)
        email= request.POST['email']
        password = request.POST['password']
        print("in post method")
        print("email",email,"password",password)

        try:
            user = User.objects.get(email=email)
            print("user value",user)
            user = authenticate(username= user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'logged in')
                print("logged in user is ",user)
                return render(request,'index.html',locals())
            else:
                 messages.error(request, "Invalid Credentials")
                 return HttpResponseRedirect("login")
        except Exception as e:
            print(e)
            messages.error(request, 'User not exists with given username')
            return HttpResponseRedirect("login")


##################################logout###################
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("login")    

          
    


    # class CartItem(View):
    #     def get(self,request):
    #         return render(request,'product-cart.html')

    #     def post(self,request):
    #         pass

    #     def update(self,request):
    #         pass

    #     def delete(self,request):
    #         pass

# class Product(View):
#     def get(self,request):
#         print(request.user,'==========request.user')
#         if request.user.is_staff:
#             return render(request,'product-list.html')
#         return HttpResponse("you cannot access this page!")
 

#     def post(self,request):
#         print(request.POST)
#         user = request.POST.get('user')
#         price = request.POST.get('price ')
#         quantity = request.POST.get('quantity')
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#         image = request.POST.get('image')
#         obj = Products(user=user,price=price,quantity=quantity,title=title,image=image)
#         obj.save()

#         return render(request,'product-edit.html')




class Addproduct(View):
    def get(self,request):
        print(request.user,'============')
        return render(request,'product-edit.html')
    def post(self,request):
        print(request.POST)
        userr = User.objects.get(username=request.user)
        price = request.POST.get('price')
        print(price,'===========price')
        quantity = request.POST.get('quantity')
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        obj = Products(user=userr,price=price,quantity=quantity,title=title,description=description,image=image)
        obj.save()
        return render(request,'product-edit.html',locals())


def Show(request):
     p=Products.objects.all()
     return render(request,'product-list.html',locals())

def Add_to_cart(request,id):
        if request.user.is_authenticated():
             try:
                 book = Products.objects.get(id=id)
             except ObjectDoesNotExist:
               pass
        else :
                try:
                    cart = Cart.objects.get(user = request.user, is_submit = False)
                except ObjectDoesNotExist:
                     cart = Cart.objects.create(user = request.user)
                     cart.save()
                    # cart.add_to_cart(Product_id)
                     return HttpResponseRedirect("product-list.html")
    
                else:
                     return redirect('index')

class AddToCart(View):
    def get(self,request):
        products = Products.objects.all()
        return render(request,'product-cart.html', locals())
    
    def post(self,request):
        product_id = request.POST.get('product_id')
        qty =  request.POST.get('qty')

        try:        
            cart, created = Cart.objects.get_or_create(user=request.user)
            product = Products.objects.get(pk=product_id)
            if int(qty) <= int(product.quantity):
                item, item_created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
                item.quantity = qty
                item.save()
                product.quantity = product.quantity - int(qty)
                product.save()
                status = True
                msg = "Saved"
            else:
                status = False
                msg = "Quantity should be less than total qty"
        except Products.DoesNotExist:
            status = False
            msg = "Invalid Product"
        return HttpResponse(json.dumps({'status': status, 'msg':msg}), 
            content_type='application/json')



class Remove_from_cart(View):

    def post(self,request):
        product_id = request.POST.get('product_id')
        try:        
            product = Products.objects.get(pk=product_id)
            item = CartItem.objects.get(cart__user=request.user, product_id=product_id)
            qty = item.quantity
            item.delete()
            product.quantity = product.quantity + int(qty)
            product.save()
            status = True
            msg = "Deleted"

        except Products.DoesNotExist:
            status = False
            msg = "Invalid Product"
        return HttpResponse(json.dumps({'status': status, 'msg':msg}), 
            content_type='application/json')


def upd(request,id):
    if request.method == "POST":
        print(request.POST)
        data = {
            'status' : False
        }
  
        try:
            p = Products.objects.get(id = id)
            name = request.POST.get('username')
            price = request.POST.get('price')
            quantity = request.POST.get('quantity')
            title = request.POST.get('title')
            description = request.POST.get('description')
            image = request.POST.get('image')
            p.save()
            return render(request,'product-list.html')
        
        except Exception as e:
              data['message'] = "not-updated!"
        
        #  finally:
#             # print("b4 sleep")
#             # sleep(10)
#             # print("after sleepo")
#             return HttpResponse(json.dumps(data), content_type="application/json")

#     else:
#         p = Product.objects.get(id = id)
        return render(request,"product-list.html",locals())

class Payment(TemplateView):
    template_name="product-payment.html"

    def get(self,request):
        cart = Cart.objects.filter(user=request.user, is_submit=False).last()
        print(cart,'========cart')
        return render(request,self.template_name, locals())

    def post(self,request):
        address = request.POST.get('addr')
        cart_id = request.POST.get('cart_id')
        print(address)
        print(cart_id)
        # data = Cart.objects.get(id=cart_id)
        # data.Address= address
        data = Cart.objects.filter(id= cart_id).update(Address=address)
    

        
        # client = User.objects.get(username=name)
        # data= Cart.objects.create(user=client,Address=address)
        # data.save()



        # return HttpResponse("Data Saved Successfully")



# def create_checkout_session(request):
#     if request.method == 'GET':
#         domain_url = 'http://localhost:8000/'
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         try:
#             checkout_session = stripe.checkout.Session.create(
#                 # new
#                 client_reference_id=request.user.id if request.user.is_authenticated else None,
#                 success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
#                 cancel_url=domain_url + 'cancelled/',
#                 payment_method_types=['card'],
#                 mode='payment',
#                 line_items=[
#                     {
#                         'name': 'Tshirt',
#                         'quantity': 1,
#                         'currency': 'INR',
#                         'amount': '20',
#                     }
#                 ]
#             )
#             return HttpResponse("success")
#         except Exception as e:
#             return HttpResponse("failed")


# class SuccessView(TemplateView):
#     template_name = 'success.html'


# class CancelledView(TemplateView):
#     template_name = 'cancelled.html'

class Showproduct(View):

    def get(self,request):
       cartitem = CartItem.objects.all()
       return render(request,'payment.html', locals())
    def post(self,request):
        
        print(request.POST)
        # price_id =  'price_1KC2JXSJi6pCV3fKSG57y83k'
        price_id = request.POST.get('price_id')
        print(price_id)

        stripe.api_key = settings.STRIPE_SECRET_KEY

        session = stripe.checkout.Session.create(
            success_url='http://127.0.0.1:8000/success/?session_id={CHECKOUT_SESSION_ID}&pid='+str(price_id),
            cancel_url='http://127.0.0.1:8000/cancel',
            payment_method_types=['card'],
            mode='payment',
             line_items=[
                    {
                        'name': 'T-shirt',
                        'quantity': 1,
                        'currency': 'inr',
                        'amount' : 2000
                    }]
        )
        response = {
            'status':True,
            'session_url':session.url
        }
        # return redirect(session.url, code=303)
        return HttpResponse(json.dumps(response), content_type='application/json')
    # def post(self,request):
    
    
    


    





class success(View):
    template_name = "courses/success.html"

    def get(self,request):
        stripe.api_key = settings.STRIPE_PRIVATE_KEY
        try:
            session_id=request.GET['session_id']
            price_id = request.GET['pid']
            session = stripe.checkout.Session.retrieve(request.GET['session_id'])
            customer = stripe.Customer.retrieve(session.customer)
            print(customer)

            level1= 'price_1JFuw3SIibBGQfNwK4550NlE'
            level2= 'price_1JFuxESIibBGQfNwRbcZ85X0'
            level3= 'price_1JFuxkSIibBGQfNwOfqMJxG3'
            try:
                x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
                external_ip = x_forward.split(",")[0]
            except:
                external_ip = request.META.get("REMOTE_ADDR")

            user = request.user


            try:
                already_member = PremiumMembers.objects.get(user = request.user)
                print("already a member")
            except Exception as e:
                print("not a member already")
            finally:
                print("----======-----====----==--==-=-=-=-=")
                member = PremiumMembers()
                member.session_id = session_id
                member.user = request.user
                member.save()

                profile = request.user.profile
                print(profile.isPremium)

                if(price_id == level1):
                    profile.isPremium = "p-1"
                    profile.save()
                    createLog(external_ip, user, "start Premium(p1)", "Premium User Feature", course_id=0, video_id=0)

                elif(price_id == level2):
                    profile.isPremium = "p-2"
                    profile.save()
                    createLog(external_ip, user, "start Premium(p2)", "Premium User Feature", course_id=0, video_id=0)

                elif(price_id == level3):
                    profile.isPremium  = "p-3"
                    profile.save()
                    createLog(external_ip, user, "start Premium(p3)", "Premium User Feature", course_id=0, video_id=0)





            # stripe.InvoiceItem.create(
            #     price=price_id,
            #     customer=customer.get('id'),
            # )

            # invoice = stripe.Invoice.create(
            #     customer=customer.get('id'),
            #     collection_method='send_invoice',
            #     days_until_due=30,
            # )
            # invoice.send_invoice()
            # print(invoice)

            # invoice = stripe.Invoice.create(
            #     customer=customer.get('id'),
            #     stripe_account='acct_1IutOESIibBGQfNw',
            # )
            # print(invoice)

        except Exception as e:
            print("-----exception block outer-------")
            print(e)

        return render(request,self.template_name,locals())

# def stripetest(request):
  
#     return HttpResponse("testing")
    


 