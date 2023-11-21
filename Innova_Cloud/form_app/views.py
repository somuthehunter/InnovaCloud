from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import pickle
import numpy as np

# Load the trained model
with open('models/model_tree.pkl', 'rb') as model_file:
    model = pickle.load(model_file)


# Create your views here.
@login_required(login_url='login')
def homepage(request):
    return render(request,'home.html')
def signuppage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        
        if(pass1!=pass2):
            return HttpResponse("not same")
    
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        
        
        
    return render(request,'signup.html')

def loginpage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!!!")
        
    
    
    return render(request,'login.html')

def logoutpage(request):
    logout(request)
    return redirect('login')

def prediction(request):
    return render(request,'prediction.html')


def train_model(request):
    if request.method == "POST":
        features = [float(request.POST.get('Temp_C')), float(request.POST.get('Dew Point Temp_C')),
                    float(request.POST.get('Rel Hum_%')),float(request.POST.get('Wind Speed_km/h')),
                    float(request.POST.get('Visibility_km')),float(request.POST.get('Press_kPa')),
                      float(request.POST.get('rain'))  ]
        # # Get user input
        # features.append( float(request.POST.get("Temp_C")))
        # features.append( float(request.POST.get("Dew point Temp_c")))
        # features.append( float(request.POST.get("Rel humidity_%:")))
        # features.append( float(request.POST.get("Wind speed_km/h")))
        # features.append( float(request.POST.get("Visibility_km -visibility")))
        # features.append( float(request.POST.get("Press_kPa")))
        # # features.append( request.POST.get("Weather"))
        # features.append( float(request.POST.get("rain -> per inch")))

        features = np.asarray(features).reshape(1,-1)
        prediction = model.predict(features)

        return JsonResponse({"prediction": prediction[0]})
    # else:
    #     # Handle the case where user_input is None
    #     features = 0.0  # or any other default value
    return render(request,'cloudburst.html')