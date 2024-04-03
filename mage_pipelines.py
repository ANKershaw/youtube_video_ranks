import sys
import time
import requests
import os


def make_api_call(url, method):
	try:
		if method == 'GET':
			response = requests.get(url)
		if method == 'POST':
			response = requests.post(url)
		# Check if the request was successful
		# (status code 200)
		if response.status_code == 200:
			# Assuming the response is JSON data
			data = response.json()
			return data
		else:
			print(f"Failed to fetch data. Status code: {response.status_code}")
			return None
	except requests.exceptions.RequestException as e:
		print(f"Error fetching data: {e}")
		return None


def exit_program():
	print("Exiting the program...")
	sys.exit(0)


def status_check(job_id):
	pipeline_status_url = "http://localhost:6789/api/pipeline_runs"
	start_time = time.time()
	while True:
		status_data = make_api_call(pipeline_status_url, "GET")
		
		if status_data:
			status = ""
			parsed_data = status_data['pipeline_runs']
			for run in parsed_data:
				if run['id'] == job_id:
					status = run['status']
					elapsed_time = time.time() - start_time
					print(f'....{elapsed_time:>3.0f}s. status: {status}')
					if status == "completed":
						print(f'pipeline is complete!')
						return
					if status == "failed" or status == "cancelled":
						print(f'pipeline encountered an error. check the logs and try again.')
						exit_program()
		else:
			print(f'api encountered an error. check the logs and try again.')
			exit_program()
		
		time.sleep(5)

def phase_1():
	# this phase writes data from api to google cloud storage bucket
	phase_one_url = "http://localhost:6789/api/pipeline_schedules/1/pipeline_runs/3ffcd4276d7b47cd890e60b828bc633c"
	# call the function to make the API call
	api_data = make_api_call(phase_one_url, "POST")
	if api_data:
		print(f"running pipeline 1 with id: {api_data['pipeline_run']['id']}")
		status_check(api_data['pipeline_run']['id'])
		keep_going = input("you now have api data saved to GCS bucket. do you want to run the second pipeline? (y/n)").lower()
		if keep_going == "y" or keep_going == "yes":
			phase_2()
		else:
			print("exiting.")
			exit_program()
def phase_2():
	# this phase writes data from google cloud storage bucket to bigquery
	phase_two_url = "http://localhost:6789/api/pipeline_schedules/2/pipeline_runs/afeb3a6f90a943e0ab61de1c14b41181"
	api_data = make_api_call(phase_two_url, "POST")
	if api_data:
		print(f"running phase 2 with id: {api_data['pipeline_run']['id']}")
		status_check(api_data['pipeline_run']['id'])
		keep_going = input("you now have gcs data saved to BigQuery tables. do you want to run the dbt pipeline? (y/n)").lower()
		if keep_going == "y" or keep_going == "yes":
			phase_3()
		else:
			print("exiting.")
			exit_program()
			
def phase_3():
	# this phase executes the dbt seed and build operations to create BigQuery views
	phase_three_url = "http://localhost:6789/api/pipeline_schedules/3/pipeline_runs/b6a9d107b2e74927b552bce51e848501"
	api_data = make_api_call(phase_three_url, "POST")
	if api_data:
		print(f"running phase 3 with id: {api_data['pipeline_run']['id']}")
		status_check(api_data['pipeline_run']['id'])
		print("you now have views in BigQuery")


def main():

	phase_number = input("""Which pipeline do you want to run?
1) api to gcs folder
2) gcs folder to bigquery
3) dbt build
	""").strip(" ")
	if phase_number == 1:
		phase_1()
	
	if phase_number == 2:
		phase_2()
	
	if phase_number == 3:
		phase_3()
		
	else:
		print("no pipeline selected. exiting.")
		exit_program()

		
if __name__ == "__main__":
	main()
