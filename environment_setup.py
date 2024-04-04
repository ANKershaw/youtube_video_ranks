import os


def file_exists(file_path):
    return os.path.exists(file_path)


def main():
    terraform_tfvars_file = "terraform/terraform.tfvars"
    env_file = "mage/.env"
    mage_start_win = "mage/mage_start.bat"
    mage_start_unix = "mage/mage_start.sh"
    file_list = [terraform_tfvars_file, env_file, mage_start_win, mage_start_unix]
    
    # Ask user for input
    gcs_project_name = input("What is your Google Cloud project name: ").strip(" ").replace("'", "").replace('"', '')
    
    gcs_bucket_name = (input("What is the name of the bucket you want created?\n(note: this must be a unique name): ")
                       .strip(" ").replace("'", "").replace('"', ''))
    
    gcs_location_name = (input("In which geographical location is the bucket to be created?\n(default: US): ")
                         .strip(" ").replace("'", "").replace('"', ''))
    if len(gcs_location_name) == 0:
        gcs_location_name = "US"
        print("Using default: US")
        
    gcs_region_name = (input("In which region would you like your bucket located?\n(default: us-west1):").strip(" ")
                       .replace("'", "").replace('"', ''))
    if len(gcs_region_name) == 0:
        gcs_region_name = "us-west1"
        print("Using default: us-west1")
    
    gcs_key_location = (input("""What is the full path + filename of your Google Cloud account key?
(eg:/Users/username/keys/service_account_key.json): """).strip(" ").
                        replace("'", "").replace('"', ''))
    
    # Ask user to confirm the input
    confirm = input(f"""Is the input correct?
    project name: {gcs_project_name}
    bucket name: {gcs_bucket_name}
    gcs location: {gcs_location_name}
    bucket region: {gcs_region_name}
    key location: {gcs_key_location}
    (yes/no, default: yes): """).lower()
    
    if len(confirm) == 0:
        confirm = "yes"
    
    # Check if the input is correct
    if confirm == "yes" or confirm == "y":
        # Open a file in write mode
        with open(terraform_tfvars_file, "w") as file:
            # Write the user input to the file
            file.write(f"""
project = "{gcs_project_name}"
location = "{gcs_location_name}"
region = "{gcs_region_name}"
gcs_bucket = "{gcs_bucket_name}"
auth_key = "{gcs_key_location}"
            """)
        
        key_directory_path, key_filename = os.path.split(gcs_key_location)
        with open(env_file, "w") as file:
            file.write(f"""GOOGLE_APPLICATION_CREDENTIALS=/home/keys/{key_filename}
GCS_BUCKET_NAME={gcs_bucket_name}
GCS_PROJECT_NAME={gcs_project_name}
            """)
        
        with open(mage_start_win, "w") as file:
            file.write(f"""docker run -it -p 6789:6789 -v $(pwd):/home/src -v {key_directory_path}:/home/keys --env-file .env mageai/mageai
            """)
            
        with open(mage_start_unix, "w") as file:
            file.write(f"""#!/bin/bash
docker run -it -p 6789:6789 -v $(pwd):/home/src -v {key_directory_path}:/home/keys --env-file .env mageai/mageai
                 """)

        print(f"Values have been written to the following files:")
        print('\n'.join([f"   {file}" for file in file_list]))
        
    else:
        print("Input was not confirmed. Exiting...")
        

if __name__ == "__main__":
    main()
