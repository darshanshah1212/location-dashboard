from django.contrib import admin
from django.urls import path 
from dashboard import views


urlpatterns = [
    path('',views.login_page,name="login_page"),
    path('dashboard/',views.dashboard,name="dashboard"),
    
    #country part
    path('countries/',views.country_page,name="country_page"),
    path('countries/list/',views.country_list,name="country_list"),
    path('countries/add/',views.add_country,name="add_country"),
    path('countries/delete/<int:pk>/',views.delete_country, name='delete_country'),
    path('countries/edit/<int:id>/',views.edit_country, name='edit_country'),
    
    #State part
    path('state/',views.state_page,name="state_page"),
    path('state/list/',views.state_list,name="state_list"),
    path('state/add/',views.add_state,name="add_state"),
    path('state/edit/<int:id>/',views.edit_state,name="edit_state"),
    path('state/delete/<int:id>/',views.delete_state,name="delete_state"),
    
    #City Part
    path('city/',views.city_page,name="city_page"),
    path('city/get_states/<int:country_id>/',views.get_states,name="get_states"),
    path('city/list/',views.city_list,name="city_list"),
    path('city/add/',views.add_city,name="add_city"),
    path('city/edit/<int:id>/',views.edit_city,name="edit_city"),
    path('city/delete/<int:id>/',views.delete_city,name="delete_city"),
    
    
    #All Part
    path('all/',views.all_page,name="all_page"),
    path('get-all-states/<int:country_id>/',views.get_all_states,name="get_all_states"),
    path('get-all-city/<int:state_id>/',views.get_all_city,name="get_all_city"),
    
    #User_Manage
    path('user-manage/',views.user_manage,name="user_manage"),
    path('user/user-list/',views.user_list,name="user_list"),
    path('user/add/',views.add_user,name="add_user"),
    path('user/delete/<int:user_id>/',views.delete_user,name="delete_user"),
    path('user/update/<int:user_id>/',views.update_user,name="update_user"),
    path('get-states/<int:country_id>/',views.state_all,name="state_all"),
    path('get-cities/<int:state_id>/',views.cities_all,name="cities_all")
]
