from django.shortcuts import render
import csv, os
from datetime import datetime
from .models import Temp1, Temp2, Ph1, Ph2, BatchInfo
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

BATCH_IDS = ('AP400E0101', 'AP400E0102', 'BP400E0101', 'BP400E0102', 'CP400E0101', 'CP400E0102')

def batch_view(request, batch_id = BATCH_IDS[0]):

    batch_info = get_object_or_404(BatchInfo, batch_id=batch_id) 

    context = {}
    context['batch_ids'] = BATCH_IDS
    context['batch_info'] = batch_info 
    
    models = (Temp1, Temp2, Ph1, Ph2)
    sensors = ('400E_Temp1', '400E_Temp2', '400E_PH1', '400E_PH2')
    sensor_batches = {}

    # Prepare sensor data 
    for model, sensor in zip(models, sensors):
        print(batch_info.start_date, batch_info.end_date)
        sensor_batch = model.objects.filter(
            timestamp__gt=batch_info.start_date, timestamp__lt=batch_info.end_date)
        sensor_batches[sensor] = sensor_batch 
        context[sensor] = [
            {'x':str(data.timestamp), 'y':data.value} for data in sensor_batch
        ]   

    # Count number of time steps in batch
    context['time_steps'] = sensor_batch.count()  
       
    # Prepare sensor temperature difference data
    temp1 = sensor_batches['400E_Temp1'] 
    temp2 = sensor_batches['400E_Temp2'] 
    temp_diffs = [
        {'x':str(temp1.timestamp), 'y':(temp1.value - temp2.value)}
         for (temp1, temp2) in zip(temp1, temp2)
    ]
    context['temp_diffs'] = temp_diffs

    # Prepare sensor PH difference data
    ph1 = sensor_batches['400E_PH1'] 
    ph2 = sensor_batches['400E_PH2'] 
    ph_diffs = [
        {'x':str(ph1.timestamp), 'y':(ph1.value - ph2.value)} 
         for (ph1, ph2) in zip(ph1, ph2)
        ]
    context['ph_diffs'] = ph_diffs
    
    return render(request, "visualizer/batches.html", context)


def home_view(request):
    batches = BatchInfo.objects.all()
    return render(request, "visualizer/home.html", {'batches':batches})

def about_view(request):
    return render(request, "visualizer/about.html")
    