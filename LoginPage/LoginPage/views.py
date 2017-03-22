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

def home_page(request):
	return render_to_response('html_templates/homepage.html')


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

	client=Client.objects.create(mob_no= u_mobno, user=user, email=email)

	return render_to_response('html_templates/login.html')

#	return HttpResponse(json.dumps({'validation':'registraion succesfully', 'status':True}), content_type="application/json")


def get_user(user):
	print user
	user_info = User.objects.get(username=user)
	client_info = Client.objects.get(user=user)

	first_name = user_info.first_name
	last_name = user_info.last_name
	email = user_info.email
	mobile_no = client_info.mob_no

	queryset = {"first name":first_name ,
		"last_name":last_name ,'email':email , "mobile_no":mobile_no}
	print queryset

	user_list = {"data" : queryset }
#	return queryset
	return user_list
#	return render_to_response('html_templates/getuser.html', user_list)



def login(request):
	jsonobj=request.POST
	print (jsonobj)

	user_name=jsonobj.get("user_name")
	password=jsonobj.get("password")
	print user_name,password

	if user_name == None:
		return HttpResponse(json.dumps({'validation':'Enter email' , "status": False}), content_type="application/json")
	if password == None:
		return HttpResponse(json.dumps({'validation':'Enter password first' , "status": False}), content_type="application/json")

	userdetail = Client.objects.all()
	for i in userdetail:
		print i
		if i.email == user_name or str(i.mob_no) == user_name:
			user_st = i.user
			user = authenticate(username= user_st,password=password)
			if not user:
				return HttpResponse(json.dumps({'validation':'Invalid user', "status": False}), content_type="application/json")
			if not user.is_active:
				return HttpResponse(json.dumps({'validation':'The password is valid, but the account has been disabled!', "status":False}), content_type="application/json")
			auth_login(request,user)
	queryset = get_user(user)
	return render_to_response('html_templates/getuser.html',queryset)
#	return HttpResponse(json.dumps({'validation':'Login successfully', "status": True}), content_type="application/json")



def logout_view(user):
	logout(user)
	return render_to_response('html_templates/homepage.html')


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

#def get_user(request):
#	jsonobj=json.loads(request.body)
#	print(jsonobj)
#
#	username = jsonobj.get('UserName')
#
#	user = Client.objects.filter(user__username='username')
#
#	data=[]
#	for i in user:
#		data.append({"first name":i.first_name ,
#		"last_name":i.last_name , "mob_no":i.mob_no ,'email':i.email })
#	print data
#
#	user_list = {"data" : data }
#
#	return render_to_response('html_templates/user_search.html', user_list)


#def show_student(user):
#
#   student_info = StudentInfo.objects.get(name=user)
#
#   name = student_info.name
#   lib_no = student_info.lib_no
#
#   books = BookDetail.objects.all()
#
#   queryset = { "name":name,
#                   "lib_no":lib_no,
#                       "books":books
#           }
#
#   return queryset

def get_all(request):
	jsonobj=json.loads(request.body)

	all_users = Client.objects.all()

	dic = {"data":all_users}

	return render_to_response('html_templates/user_search.html',dic)
