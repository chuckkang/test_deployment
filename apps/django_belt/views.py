from django.shortcuts import render, redirect, HttpResponse
from models import *
def index(request):
	
	return render(request, "django_belt/index.html")

def main(request):
	if (valid_session(request)==False):
		return redirect('/')
	# print request.session['user_id'], "check_session"
	return render(request, "django_belt/main.html")

def login(request):
	#check the login credentials
	formdata={}
	if request.method=='POST':
		email = request.POST['email'].strip().lower()
		password = request.POST['password'].strip()
		validlogin = User.objects.login_validation(request.POST)
		if validlogin == True:
			user = User.objects.get(email=email)
			request.session['user_id'] = user.id
			messages.add_message(request, messages.INFO, "You have logged in successfully!")
			return redirect('/main')
		else:
			messages.add_message(request, messages.INFO, validlogin)
	else:
		formdata={'loginemail': request.POST['email'].strip().lower()}
	return render(request, 'django_belt/index.html', formdata)
	

def register(request):
	formdata={}
	if request.method=='POST':
		error = User.objects.registration_validation(request.POST)
		first_name = request.POST['first_name'].strip()
		last_name = request.POST['last_name'].strip()
		email = request.POST['email'].strip().lower()
		password = request.POST['password'].strip()
		formdata={ #send this basic information back -- Do not return sensitive information -- this is to populate the form
			'first_name': first_name,
			'last_name': last_name,
			'email': email
		}
		if len(error)!=0:
			messages.add_message(request, messages.INFO, error)
		else:
			password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			user_id = User.objects.create(first_name=first_name , last_name=last_name, email=email , password=password)
			if (user_id.id):
				messages.add_message(request, messages.INFO, "You registered succesfully!")
				request.session['user_id'] = user_id.id
			return redirect('/main')
	else:
		messages.add_message(request, messages.INFO, "You must first login to access this site")
		request.session.clear()
		
	return render(request, 'django_belt/index.html', formdata)

def logout(request):
	request.session['user_id']=0
	return redirect('/')

def valid_session(request):
	isValid = True
	if ('user_id' not in request.session):
		request.session.clear()
		isValid = False
	else:
		if request.session['user_id']==0:
			request.session.clear()
			isValid = False

	return isValid