from django.db import models
import os, csv
from datetime import datetime


class BatchInfo(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration = models.DurationField()
    batch_id = models.CharField(max_length=10)

class Temp1(models.Model):
    timestamp = models.DateTimeField(primary_key=True)
    value = models.FloatField()
    
class Temp2(models.Model):
    timestamp = models.DateTimeField(primary_key=True)
    value = models.FloatField()
    
class Ph1(models.Model):
    timestamp = models.DateTimeField(primary_key=True)
    value = models.FloatField()
    
class Ph2(models.Model):
    timestamp = models.DateTimeField(primary_key=True)
    value = models.FloatField()
    

def load_data():
    """
    Loads data from csv-files into tables. 
    When loading batch info data, the duration of each batch is also calculated and stored. 
    
    Execute in django shell with these commands:
    $ make shell  (opens up django shell in running container)
    >>>from visualizer.models import load_data
    >>>load_data()
    """
    # Delete all data
    Temp1.objects.all().delete()
    Temp2.objects.all().delete()
    Ph1.objects.all().delete()
    Ph2.objects.all().delete()
    BatchInfo.objects.all().delete()

    # Data path
    data_path = os.path.join(os.path.dirname(__file__), 'data')
 
    # Load batch meta data    
    batch_info_csv_path = os.path.join(data_path, 'batch_info.csv')
    with open(batch_info_csv_path) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        next(reader)
        
        for batch in reader:            
            # We need to convert time to datetime objects to calculate duration
            start_date = datetime.strptime(batch[0],'%Y-%m-%d %H:%M:%S')
            end_date = datetime.strptime(batch[1],'%Y-%m-%d %H:%M:%S')
           
            BatchInfo.objects.get_or_create(
                start_date = start_date,
                end_date = end_date,
                duration = end_date - start_date, 
                batch_id = batch[2].strip()
            )

    # Load sensor data
    sensors = ('400E_PH1', '400E_PH2', '400E_Temp1', '400E_Temp2')
    models = (Ph1, Ph2, Temp1, Temp2)
    for sensor, model in zip(sensors, models):
        sensor_csv_path = os.path.join(data_path, sensor + '.csv')
        with open(sensor_csv_path) as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            for row in reader:
                model.objects.create(
                    timestamp = datetime.strptime(row['timestamp'],'%Y-%m-%d %H:%M:%S'),
                    value=row['value'],
                )
    
    # Print some logging to django shell
    print(f"Loaded {BatchInfo.objects.all().count()} rows of meta data (should be 18).")
    for sensor, model in zip(sensors, models):
        print(f"Loaded {model.objects.all().count()} rows from {sensor}.csv (should be 14207 or 14206).")
    

