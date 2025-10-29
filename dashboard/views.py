from django.shortcuts import render ,redirect , get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator
from .models import State,Country,City,UserManage
from .forms import UserManageForm


# Create your views here.
def login_page(request):
    if request.method == 'POST':
        return render(request,'dashboard.html')
    return render(request,'login.html')


def dashboard(request):
    return render(request,'dashboard.html')

#-------------------------------------------------------Country Section------------------------------------------------------------#
def country_page(request):
    return render(request, 'country.html')

def add_country(request):
    name = request.POST.get("name","").strip()
    if not name:
        return JsonResponse({"status": "error", "message": "Name is required"})
    if Country.objects.filter(name__iexact=name).exists():
        return JsonResponse({"status":'error','message':'Country already Exist'})
    c = Country.objects.create(name=name)
    return JsonResponse({'status':'success','id':c.id, 'name':c.name})

def country_list(request):
    page = int(request.GET.get('page',1))
    countries = Country.objects.all().order_by("-id")
    paginator = Paginator(countries,10)
    page_obj = paginator.get_page(page)
    
    data = []
    for idx, c in enumerate(page_obj,start=page_obj.start_index()):
        data.append({'id':c.id,'no':idx,'name':c.name})
        
    return JsonResponse({
        'countries':data,
        'pages': list(paginator.page_range),
        'current':page_obj.number
    })
    
        
def delete_country(request,pk):
    if request.method == 'POST':
        country = get_object_or_404(Country,pk=pk)
        country.delete()
        return JsonResponse({'status':'success','message':'Deleted successully'})
    return JsonResponse({'status':'error','message':'Invalid Request'})


def edit_country(request,id):
    if request.method == 'POST':
        name = request.POST.get("name","").strip()
        if not name:
            return JsonResponse({"status":"error","message":"Name Required"})
        
        if Country.objects.filter(name__iexact=name).exclude(id=id).exists():
            return JsonResponse({"status":"error","message":"Data Already Exist"})
        
        country = Country.objects.get(id=id)
        country.name = name
        country.save()
        return JsonResponse({"status":"success"})
    return JsonResponse({'status':'error','message':'Invalid Request'})

#-------------------------------------------------------State Section------------------------------------------------------------#

def state_page(request):
    countries = Country.objects.all()
    return render(request, 'state.html', {'countries': countries})

def add_state(request):
    if request.method == "POST":
        country_id = request.POST.get("country_id")
        state_name = request.POST.get("state_name").strip()

        if not state_name:
            return JsonResponse({"status":"error","message":"State name is required"})

        country = Country.objects.get(id=country_id)

        if State.objects.filter(country=country, name__iexact=state_name).exists():
            return JsonResponse({"status":"error","message":"State already exists for this country"})

        State.objects.create(country=country, name=state_name)
        return JsonResponse({"status":"success","message":"Data Inserted"})

    
def state_list(request):
    page = int(request.GET.get('page', 1))
    countries = Country.objects.prefetch_related('states').all().order_by('-id')

    data = []
    for country in countries:
        states = [{'id': s.id, 'name': s.name , 'country_id':country.id} for s in country.states.all()]
        if states:
            data.append({
                'country_id': country.id,
                'country_name': country.name,
                'states': states
            })

    per_page = 5
    total_pages = (len(data) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paged_data = data[start:end]

    return JsonResponse({
        'countries': paged_data,
        'pages': list(range(1, total_pages+1)),
        'current': page
    })
    

def delete_state(request,id):
    if request.method == 'POST':
        state = get_object_or_404(State,id=id)
        state.delete()
        return JsonResponse({'status':'success','message':'Deleted successfully'})
    return JsonResponse({'status':'error','message':'invalid Request'})
       
       
def edit_state(request,id):
    if request.method == 'POST':
        name = request.POST.get('name','').strip()
        
        country_id = request.POST.get("country_id")
        
        state = State.objects.get(id=id)
        
        if country_id:
            state.country_id = country_id
        if not name:
            return JsonResponse({'status':'error','message':'State Requiered'})
        
        if State.objects.filter(name__iexact=name, country=state.country).exclude(id=id).exists():
            return JsonResponse({'status':'error','message':'State already exists in the country'})

        state.name = name
        state.save()
        return JsonResponse({'status':'success'})
    return JsonResponse({'status':'error','message':'Invalid Request'})
    

#-------------------------------------------------------City Section------------------------------------------------------------#

def city_page(request):
    countries = Country.objects.all()
    return render(request,'city.html',{'countries':countries})

def get_states(request,country_id):
    states = State.objects.filter(country_id=country_id).values('id', 'name')
    return JsonResponse({"states":list(states)})
    
    
def city_list(request):
    page = int(request.GET.get("page", 1))
    cities = City.objects.select_related("state__country").all().order_by("-id")
    paginator = Paginator(cities, 10)
    page_obj = paginator.get_page(page)

    grouped = {}
    for city in page_obj:
        country = city.state.country.name
        state = city.state.name
        if country not in grouped:
            grouped[country] = {}
        if state not in grouped[country]:
            grouped[country][state] = []
        grouped[country][state].append({"id": city.id, "name": city.name,"state_id":city.state_id,"country_id":city.state.country.id})

    return JsonResponse({
        "countries": grouped,
        "pages": list(range(1, paginator.num_pages + 1)),
        "current": page_obj.number
    })
    
def add_city(request):
    if request.method == 'POST':
        state_id = request.POST.get("state_id")
        name = request.POST.get("name")
        
        if not state_id or not name:
            return JsonResponse({"status":"error","message":"State and City required"})
        
        if City.objects.filter(name__iexact=name,state_id=state_id).exists():
            return JsonResponse({"status":"error","message":"City Already Exists"})
        
        City.objects.create(name=name , state_id=state_id)
        return JsonResponse({"status":"success"})
    
    return JsonResponse({"status":"error","message":"Invalid Req"})


def edit_city(request,id):
    if request.method == 'POST':
        name = request.POST.get('name','').strip()
        state_id = request.POST.get("state_id")
        
        city = City.objects.get(id=id)
        
        if not name:
            return JsonResponse({"status":"error","message":"City Required"})
        
        if City.objects.filter(name__iexact=name,state=city.state,state_id=state_id).exclude(id=id).exists():
            return JsonResponse({"status":"error","message":"City already exists in State"})
        
        city.name=name
        city.state_id = state_id
        city.save()
        return JsonResponse({"status":"success"})
    return JsonResponse({"status":"error","message":"Invalid Request"})


def delete_city(request,id):
    if request.method == "POST":
        city = get_object_or_404(City,id=id)
        city.delete()
        return JsonResponse({"status":"success","message":"Deleted successfully"})
    return JsonResponse({"status":"error","message":"Invalid Request"})

#------------------------------------------------------All PART Section------------------------------------------------------------#

def all_page(request):
    countries = Country.objects.all()
    return render(request,'all.html',{'countries':countries})

def get_all_states(request,country_id):
    states =State.objects.filter(country_id=country_id).values('id','name')
    return JsonResponse({'states':list(states)})

def get_all_city(request,state_id):
    city = City.objects.filter(state_id=state_id).values('id','name')
    return JsonResponse({'city':list(city)})


#------------------------------------------------------User Management Section------------------------------------------------------------#

def user_manage(request):
    return render(request,'user_manage.html')
    
def user_list(request):
    page = int(request.GET.get('page',1))
    users = UserManage.objects.all().order_by("-id")
    paginator = Paginator(users,5)
    page_obj = paginator.get_page(page)
    
    data = {
        "users": [
            {
                "id": user.id,
                "no":idx,
                "username": user.username,
                "email": user.email,
                "phone_no": user.phone_no,
                "gender": user.gender,
                "dob": user.dob,
                "profile_photo": user.profile_photo.url if user.profile_photo else None,
                "profile_video": user.profile_video.url if user.profile_video else None,
                "bio": user.bio,
                "role": user.role,
                "country__name": user.country.name if user.country else None,
                "state__name": user.state.name if user.state else None,
                "city__name": user.city.name if user.city else None,
            }
           for idx, user in enumerate(page_obj, start=page_obj.start_index())
        ],
        "current": page_obj.number,
        "pages": list(paginator.page_range),
    }
    return JsonResponse(data)

def add_user(request):
    if request.method == 'POST':
        form =UserManageForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            user.country_id = request.POST.get("country")
            user.state_id = request.POST.get("state")
            user.city_id = request.POST.get("city")
            user.save()
            return JsonResponse({'status':'success','message':'Data Inserted Successully ! '}) 
        else:
            return JsonResponse({'status': 'error', 'message': 'Form validation failed', 'errors': form.errors})
            
        
    countries = Country.objects.all()
    return render(request,'add_user.html',{'form':UserManageForm,"countries":countries})


def state_all(request,country_id):
    states = list(State.objects.filter(country_id=country_id).values('id','name'))
    return JsonResponse({"states":states})
    
def cities_all(request,state_id):
    cities = list(City.objects.filter(state_id=state_id).values("id","name"))
    return JsonResponse({"cities":cities})

def delete_user(request,user_id):
    user = get_object_or_404(UserManage,id=user_id)
    user.delete()
    return JsonResponse({'status':'success','message':'deleted Succesfully'})

def update_user(request, user_id):
    user = get_object_or_404(UserManage, id=user_id)
    
    if request.method == 'POST':
        form = UserManageForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            update_user = form.save(commit=False)
            update_user.country_id = request.POST.get("country")
            update_user.state_id = request.POST.get("state")
            update_user.city_id = request.POST.get("city")
            update_user.save()
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "errors": form.errors})
    
    form = UserManageForm(instance=user)
    countries = Country.objects.all()
    states = State.objects.filter(country=user.country)
    cities = City.objects.filter(state=user.state)
    
    return render(request, "update_user.html", {
        'form': form,
        'user': user,
        'countries': countries,
        'states': states,
        'cities': cities
    })
    
    