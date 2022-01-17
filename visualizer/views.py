from django.shortcuts import render
from .models import Temp1, Temp2, Ph1, Ph2, BatchInfo
from django.shortcuts import get_object_or_404

BATCH_IDS = ('AP400E0101', 'TEST_001', 'AP400E0102', 'TEST_002', 'BP400E0101', 
             'BP400E0102', 'CP400E0101', 'TEST_003', 'CP400E0102')
MODELS = (Temp1, Temp2, Ph1, Ph2)
SENSORS = ('400E_Temp1', '400E_Temp2', '400E_PH1', '400E_PH2')


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

    # Prepare sensor data for timeseries chart 
    for model, sensor in zip(MODELS, SENSORS):
        sensor_batch = model.objects.filter(
             timestamp__gt=batch_info.start_date, timestamp__lt=batch_info.end_date).all() 
        context[sensor] = [{'x': str(row.timestamp), 'y': row.value} for row in sensor_batch]

    # Count number of time steps in batch (same for each sensor)
    context['time_steps'] = sensor_batch.count()
           
    return render(request, "visualizer/batches.html", context)


def deviations_view(request, batch_id = BATCH_IDS[0]):

    batch_info = get_object_or_404(BatchInfo, batch_id=batch_id) 

    context = {}
    context['batch_ids'] = BATCH_IDS
    context['batch_info'] = batch_info 

    # Query batch data for each sensor
    sensor_batches = {}
    for model, sensor in zip(MODELS, SENSORS):
        sensor_batches[sensor] = model.objects.filter(
             timestamp__gt=batch_info.start_date, timestamp__lt=batch_info.end_date).all() 
    
    # Prepare sensor temperature difference data for chart
    temp1 = sensor_batches['400E_Temp1'] 
    temp2 = sensor_batches['400E_Temp2'] 
    temp_diffs = [
        {'x':str(temp1.timestamp), 'y':(temp2.value - temp1.value)}
         for (temp1, temp2) in zip(temp1, temp2)
    ]
    context['temp_diffs'] = temp_diffs

    # Prepare sensor PH difference data for chart
    ph1 = sensor_batches['400E_PH1'] 
    ph2 = sensor_batches['400E_PH2'] 
    ph_diffs = [
        {'x':str(ph1.timestamp), 'y':(ph2.value - ph1.value)} 
         for (ph1, ph2) in zip(ph1, ph2)
        ]
    context['ph_diffs'] = ph_diffs

    # Count number of time steps in batch (same for each sensor)
    context['time_steps'] = sensor_batches['400E_Temp1'].count()

    return render(request, "visualizer/deviations.html", context)
