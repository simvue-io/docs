import simvue
import argparse
import csv
import time
import os

parser = argparse.ArgumentParser(description='Monitor alerts from a Simvue run.')
parser.add_argument(
  '--run-name', 
  type=str,
  help='The name of the run to monitor alerts for.'
  )
parser.add_argument(
  '--time-interval', 
  type=int,
  help='The interval between queries to the alert status, in seconds.'
  )
parser.add_argument(
  '--max-time', 
  type=int,
  help='The maximum time which this script will run for.'
  )
args = parser.parse_args()

script_dir = os.path.dirname(__file__)

with open(os.path.join(script_dir, 'results', 'alert_status.csv'), 'w', newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(['time', 'step_not_converged', 'temperature_exceeds_maximum', 'temperature_exceeds_melting_point'])

time_elapsed = 0
client = simvue.Client()
run_id = client.get_run_id_from_name(args.run_name)

while time_elapsed < args.max_time:
    alerts = client.get_alerts(run_id)
    with open(os.path.join(script_dir, 'results', 'alert_status.csv'), 'a', newline='') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(
            [
                time_elapsed, 
                ('Firing' if 'step_not_converged' in alerts else 'Normal'), 
                ('Firing' if 'temperature_exceeds_maximum' in alerts else 'Normal'),
                ('Firing' if 'temperature_exceeds_melting_point' in alerts else 'Normal')
            ]
          )
    
    time.sleep(args.time_interval)
    time_elapsed += args.time_interval