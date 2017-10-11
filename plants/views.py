from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from sensors.models import Sensor, SensorData, Actuator

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
        sensor1 = Sensor()
        sensor1.sensor_type = 'Temperature'
        sensor1.parent = plant
        sensor1.save()
        sensor2 = Sensor()
        sensor2.sensor_type = 'Humidity'
        sensor2.parent = plant
        sensor2.save()
        sensor3 = Sensor()
        sensor3.sensor_type = 'Soil Moisture'
        sensor3.parent = plant
        sensor3.save()
        sensor4 = Sensor()
        sensor4.sensor_type = 'Water Level'
        sensor4.parent = plant
        sensor4.save()
        sensor5 = Sensor()
        sensor5.parent = plant
        sensor5.sensor_type = 'RainSensor'
        sensor5.save()
        actuator = Actuator()
        actuator.parent = plant
        actuator.name = request.POST.get('alias')
        actuator.state = 0
        actuator.save()

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
    rain_sensor = sensors.filter(sensor_type='RainSensor')[0]
    temp_sensor = sensors.filter(sensor_type='Temperature')[0]
    hum_sensor = sensors.filter(sensor_type='Humidity')[0]
    moisture_sensor = sensors.filter(sensor_type='Soil Moisture')[0]
    wl_sensor = sensors.filter(sensor_type='Water Level')[0]
    sensor_data_temp = SensorData.objects.filter(parent=temp_sensor)
    sensor_data_hum = SensorData.objects.filter(parent=hum_sensor)
    sensor_data_wlevel = SensorData.objects.filter(parent=wl_sensor)
    sensor_data_mois = SensorData.objects.filter(parent=moisture_sensor)
    sensor_data_rain = SensorData.objects.filter(parent=rain_sensor)
    act = Actuator.objects.get(name=plant.alias)
    try:
        temp = sensor_data_temp.latest('id')
    except Exception:
        temp = None
    try:
        hum = sensor_data_hum.latest('id')
    except Exception:
        hum = None
    try:
        wlevel = sensor_data_wlevel.latest('id')
    except Exception:
        wlevel = None
    try:
        mois = sensor_data_mois.latest('id')
    except Exception:
        mois = None
    try:
        rain = sensor_data_rain.latest('id')
    except Exception:
        rain = None
    temp_values = map(lambda x: x.value, list(sensor_data_temp)[-1:-11:-1])
    soil_values = map(lambda x: x.value, list(sensor_data_mois)[-1:-11:-1])
    context={'plant': plant,
     'sensors':sensors,
     'temp': temp,
     'humidity': hum,
     'moisture': mois,
     'wlevel': wlevel,
     'rain':rain,
     'act': act,
     'temp_values':temp_values[::-1],
     'soil_values':soil_values[::-1]
     }
    print(context)
    return render(request, "plant1.html", context=context)
    return HttpResponse(str(id))