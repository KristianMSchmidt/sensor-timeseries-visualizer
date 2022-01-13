from django.shortcuts import render
import csv, os
from datetime import datetime

def home_view(request):
    batch_info_path = os.path.join(os.path.dirname(__file__), 'data', 'batch_info.csv')
    
    with open(batch_info_path) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        header = next(reader)        
        header = ['StartDate', 'EndDate', 'Duration', 'BatchId']
        batches = []
        for batch in reader:
            start_date = datetime.strptime(batch[0],'%Y-%m-%d %H:%M:%S')
            end_date = datetime.strptime(batch[1],'%Y-%m-%d %H:%M:%S')
            duration = end_date - start_date
            batch_id = batch[2]
            print(duration.total_seconds())
            batches.append([str(start_date), str(end_date), str(duration), batch_id])

    return render(request, "visualizer/home.html", {'header':header, 'batches':batches})

def about_view(request):
    return render(request, "visualizer/about.html")

def play_ground():
    print('Try out some code!')
    date_time_str_a = '18-09-19 01:55:19'
    date_time_str_b = '18-09-19 02:56:19'
    c = '2020-04-02 00:00:26'
    a = datetime.strptime(date_time_str_a, '%d-%m-%y %H:%M:%S')
    b = datetime.strptime(date_time_str_b, '%d-%m-%y %H:%M:%S')
    d=b-a
    d.seconds
    print(d.total_seconds())
if __name__ == "__main__":
    play_ground()