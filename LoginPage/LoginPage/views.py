import json
from django.http import HttpResponse
from .models import *
from django.http import JsonResponse
from django.shortcuts import render_to_response,render
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login as auth_login


# Create your views here.
def login_page(request):
	return render_to_response('html_templates/login.html')

def registration_page(request):
	return render_to_response('html_templates/registration.html')

def registration(request):
	jsonobj = request.POST
	print jsonobj

	u_mobno=jsonobj.get("Mobile_Number")

	first_name = jsonobj.get('first_name')
	last_name = jsonobj.get('last_name')
	user = jsonobj.get('User_Name')
	user_password = jsonobj.get('User_Password')
	email = jsonobj.get('email')

	if(user and first_name) == None:
		return HttpResponse(json.dumps({'validation':'name is required', 'status':False}), content_type="application/json")

	if User.objects.filter(username=user).exists():
		return HttpResponse(json.dumps({'validation':'username already exists', 'status':False}), content_type="application/json")


	user = User.objects.create(username=user,first_name = first_name,last_name=last_name,email=email,password=user_password)
	user.set_password(user_password)
	user.save()

	client=Client.objects.create(mob_no= u_mobno, user=user)

	return HttpResponse(json.dumps({'validation':'registraion succesfully', 'status':True}), content_type="application/json")

def login(request):
	jsonobj=json.loads(request.body)
	print (jsonobj)

	user_name=jsonobj.get("user_name")
	password=jsonobj.get("password")

	if email == None:
		return HttpResponse(json.dumps({'validation':'Enter email' , "status": False}), content_type="application/json")
	elif password == None:
		return HttpResponse(json.dumps({'validation':'Enter password first' , "status": False}), content_type="application/json")

	user = authenticate(username= user_name,password=password)
#	user = authenticate(username=mobile_number ,password=password)

	if not user:
		return HttpResponse(json.dumps({'validation':'Invalid user', "status": False}), content_type="application/json")
	if not user.is_active:
		return HttpResponse(json.dumps({'validation':'The password is valid, but the account has been disabled!', "status":False}), content_type="application/json")

	auth_login(request,user)
	return HttpResponse(json.dumps({'validation':'Login successfully', "status": True}), content_type="application/json")


def logout_view(request):
	logout(request)


def user_edit(request):
	jsonobj = json.loads(request.body)
	print(jsonobj)

	user_id = jsonobj.get('id')
	user_name = jsonobj.get('name')
	user_email = jsonobj.get('email')

	user_obj = User.objects.get(id = user_id)

	user_obj.username = user_name
	user_obj.email = user_email

	user_obj.save()
	return HttpResponse(json.dumps({'validation':'user updated successfully', 'status': True}), content_type="application/json")

def get_user(request):
	jsonobj=json.loads(request.body)
	print(jsonobj)

	username = jsonobj.get('UserName')

	user = Client.objects.filter(user__username='username')

	data=[]
	for i in user:
		data.append({"first name":i.first_name ,
		"last_name":i.last_name , "mob_no":i.mob_no ,'email':i.email })
	print data

	user_list = {"data" : data }

	return render_to_response('html_templates/user_search.html', user_list)
