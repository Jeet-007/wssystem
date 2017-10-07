from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from sensors.models import SensorData

from .models import Plant

# Create your views here.
@login_required(login_url='/')
@csrf_exempt
def add_plant(request):
    if request.method == 'POST':
        plant = Plant()
        if (not request.POST.get('alias')) or len(Plant.objects.filter(alias=request.POST.get('alias'), parent=request.user))!=0 :
            return HttpResponseRedirect(reverse('plants:dashboard'))        
        plant.alias = request.POST.get('alias')
        plant.parent = request.user
        plant.save()
        return HttpResponseRedirect(reverse('plants:dashboard'))
    return HttpResponseRedirect(reverse('plants:dashboard'))

@login_required(login_url='/')
def viewdashboard(request):
    plants = Plant.objects.filter(parent=request.user)
    print(plants)
    return render(request, 'userdashboard.html', {'username': request.user.username, 'plants': plants})

@login_required(login_url='/')
def plantboard(request, username):
    print (username)
    plant = Plant.objects.get(alias=username, parent=request.user)
    sensors = plant.sensor_set.all()
    print(sensors)
    temp_sensor = sensors.filter(sensor_type='Temperature')[0]
    hum_sensor = sensors.filter(sensor_type='Humidity')[0]
    moisture_sensor = sensors.filter(sensor_type='Soil Moisture')[0]
    wl_sensor = sensors.filter(sensor_type='Water Level')[0]
    sensor_data_temp = SensorData.objects.filter(parent=temp_sensor)
    sensor_data_hum = SensorData.objects.filter(parent=hum_sensor)
    sensor_data_wlevel = SensorData.objects.filter(parent=wl_sensor)
    sensor_data_mois = SensorData.objects.filter(parent=moisture_sensor)
    
    context={'plant': plant,
     'sensors':sensors,
     'temp': sensor_data_temp.latest('id'),
     'humidity': sensor_data_hum.latest('id'),
     'moisture': sensor_data_mois.latest('id'),
     'wlevel': sensor_data_wlevel.latest('id'), 
     }
    print(context)
    return render(request, "plant1.html", context=context)
    return HttpResponse(str(id))