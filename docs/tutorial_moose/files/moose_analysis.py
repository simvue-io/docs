import argparse
import simvue
import csv
import time

parser = argparse.ArgumentParser(description='Monitor alerts from a Simvue run.')
parser.add_argument(
  'run_name', 
  type=str,
  help='The name of the run to monitor alerts for.'
  )
parser.add_argument(
  'time_interval', 
  type=int,
  help='The interval between queries to the alert status, in seconds.'
  )
parser.add_argument(
  'max_time', 
  type=int,
  help='The maximum time which this script will run for.'
  )
args = parser.parse_args()

with open('tutorial/alert_status.csv', 'w', newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(['time', 'firing_alerts'])

time_elapsed = 0
client = simvue.Client()
run_id = client.get_run_id_from_name(args.run_name)

while time_elapsed < args.max_time:
    alerts = client.get_alerts(run_id)
    with open('tutorial/alert_status.csv', 'a', newline='') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow([time_elapsed, alerts])
    
    time.sleep(args.time_interval)
    time_elapsed += args.time_interval