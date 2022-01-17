from django.shortcuts import render
from .models import Temp1, Temp2, Ph1, Ph2, BatchInfo
from django.shortcuts import get_object_or_404

# Kunne også nemt hentes fra databasen
BATCH_IDS = ['AP400E0101', 'TEST_001', 'AP400E0102', 'TEST_002', 'BP400E0101', 
'BP400E0102', 'CP400E0101', 'TEST_003', 'CP400E0102']

def home_view(request):
    batches = BatchInfo.objects.all()
    return render(request, "visualizer/home.html", {'batches':batches})


def about_view(request):
    return render(request, "visualizer/about.html")   

def batch_view(request, batch_id = BATCH_IDS[0]):

    batch_info = get_object_or_404(BatchInfo, batch_id=batch_id) 

    context = {}
    context['batch_ids'] = BATCH_IDS
    context['batch_info'] = batch_info 
    
    models = (Temp1, Temp2, Ph1, Ph2)
    sensors = ('400E_Temp1', '400E_Temp2', '400E_PH1', '400E_PH2')

    # Prepare sensor data for timeseries chart 
    for model, sensor in zip(models, sensors):
        
        sensor_batch = model.objects.filter(
             timestamp__gt=batch_info.start_date, timestamp__lt=batch_info.end_date).all() 

        context[sensor] = [{'timestamp': str(row.timestamp), 'value': row.value} for row in sensor_batch]

    # Count number of time steps in batch (is the same for each sensor)
    context['time_steps'] = sensor_batch.count()
           
    return render(request, "visualizer/batches.html", context)


def deviations_view(request, batch_id = BATCH_IDS[0]):

    batch_info = get_object_or_404(BatchInfo, batch_id=batch_id) 

    context = {}
    context['batch_ids'] = BATCH_IDS
    context['batch_info'] = batch_info 

    # Query batch data for each sensor
    models = (Temp1, Temp2, Ph1, Ph2)
    sensors = ('400E_Temp1', '400E_Temp2', '400E_PH1', '400E_PH2')
    sensor_batches = {}
    for model, sensor in zip(models, sensors):
        sensor_batches[sensor] = model.objects.filter(
             timestamp__gt=batch_info.start_date, timestamp__lt=batch_info.end_date).all() 

    # Prepare sensor temperature difference data for chart
    temp1 = sensor_batches['400E_Temp1'] 
    temp2 = sensor_batches['400E_Temp2'] 
    temp_diffs = [
        {'timestamp':str(temp1.timestamp), 'value':(temp1.value - temp2.value)}
         for (temp1, temp2) in zip(temp1, temp2)
    ]
    context['temp_diffs'] = temp_diffs

    # Prepare sensor PH difference data for chart
    ph1 = sensor_batches['400E_PH1'] 
    ph2 = sensor_batches['400E_PH2'] 
    ph_diffs = [
        {'timestamp':str(ph1.timestamp), 'value':(ph1.value - ph2.value)} 
         for (ph1, ph2) in zip(ph1, ph2)
        ]
    context['ph_diffs'] = ph_diffs

    # Count number of time steps in batch
    context['time_steps'] = sensor_batches['400E_Temp1'].count()

    return render(request, "visualizer/deviations.html", context)
