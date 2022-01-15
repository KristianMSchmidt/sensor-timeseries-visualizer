from django.shortcuts import render
import csv, os
from datetime import datetime
from .models import SensorData, Batch
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
SENSORS = ('400E_PH1', '400E_PH2', '400E_Temp1', '400E_Temp2')
BATCH_IDS = ('AP400E0101', 'AP400E0102', 'BP400E0101', 'BP400E0102', 'CP400E0101', 'CP400E0102')

def timeseries_view(request, batch_id = None):
    
    batch = Batch.objects.get(batch_id=batch_id) # <- check for existen (batch id knoen?)
    batch_data = SensorData.objects.filter(timestamp__gt=batch.start_date, timestamp__lt=batch.end_date)

    context = {}
    context['batch_ids'] = BATCH_IDS

    # Prepara sensor data 
    for sensor in SENSORS:
        sensor_batch_data = batch_data.filter(sensor=sensor)
        context[sensor] = [{'x':str(data.timestamp), 'y':data.value} for data in sensor_batch_data]   
        context['data_count'] = batch_data.count()
        context['batch'] = batch 
    
    # Prepare sensor temperature difference data
    temp1 = batch_data.filter(sensor='400E_Temp1') 
    temp2 = batch_data.filter(sensor='400E_Temp2')     
    temp_diffs = [{'x':str(temp1.timestamp), 'y':(temp1.value - temp2.value)} for (temp1, temp2) in zip(temp1, temp2)]
    context['temp_diffs'] = temp_diffs

    # Prepare sensor PH difference data
    ph1 = batch_data.filter(sensor='400E_PH1') 
    ph2 = batch_data.filter(sensor='400E_PH2')     
    ph_diffs = [{'x':str(ph1.timestamp), 'y':(ph1.value - ph2.value)} for (ph1, ph2) in zip(ph1, ph2)]
    context['ph_diffs'] = ph_diffs

    return render(request, "visualizer/timeseries.html", context)


def home_view(request):
    batches = Batch.objects.all()
    return render(request, "visualizer/home.html", {'batches':batches})


def about_view(request):
    return render(request, "visualizer/about.html")

@require_POST
@login_required
def load_data_view(request):
    """
    Loads data from csv-files into tables. 
    When loading batch meta data, the duration of each batch is also calculated and stored. 
    """
    SensorData.objects.all().delete()
    Batch.objects.all().delete()

    data_path = os.path.join(os.path.dirname(__file__), 'data')
    
    # Load batch meta data
    csv_path = os.path.join(data_path, 'batch_info.csv')
    
    with open(csv_path) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        next(reader)
        
        for batch in reader:            
            # We need to convert time to datetime objects to calculate duration
            start_date = datetime.strptime(batch[0],'%Y-%m-%d %H:%M:%S')
            end_date = datetime.strptime(batch[1],'%Y-%m-%d %H:%M:%S')
           
            Batch.objects.create(
                start_date = start_date,
                end_date = end_date,
                duration = end_date - start_date, 
                batch_id = batch[2].strip()
            )

    # Load sensor data
    for sensor in SENSORS:
        csv_path = os.path.join(data_path, sensor + '.csv')

        with open(csv_path) as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            for row in reader:
                SensorData.objects.create(
                    timestamp = datetime.strptime(row['timestamp'],'%Y-%m-%d %H:%M:%S'),
                    value=row['value'],
                    sensor=sensor
                )
    
    sensor_num = SensorData.objects.all().count()
    meta_data_num = Batch.objects.all().count()

    return HttpResponse(
        f"Successfully loaded {sensor_num} rows of sensor data and {meta_data_num} " +
        "rows of meta data.<br>56827 is the correct number of sensor rows.<br>")
    

def sandbox():
    print("Hello from sandbox!")

if __name__ == "__main__":
    sandbox()