# Dropbox
A dropbox type utility with user authentication where you can upload documents by clicking on the upload link.
## Project Setup Guide:
- Clone the repository
- After going into the required directory make a vitual environment and activate it.
- Run `pip install -r requirements.txt`  to install all the requirements/dependencies preferably setup a virtual environment and then do it. 
(**Note**- Your system must have python installed (version >= 3.7.6))
- You will have to run a few migrations to make the specific tables in the database so run the following commands terminal:      
 `python manage.py migrate`        
- **Creating superuser**- This will give you the access to the admin page of the website. To make a superuser run `python manage.py createsuperuser` in the terminal and specify the details.
- Now you are good to go! Finally run `python manage.py runserver` or `python manage.py runserver <hostip>`to run the django server.

## Routes for Teacher Side website:
- `{base_url}` - home/ index page
- `{base_url}/login` - Login Page
- `{base_url}/register` - Register/ Signup page
- `{base_url}/batches` - Will show list of batches that were created by the user(teacher). On clicking a batch link from the list you can view dates on which attendance was recorded. On clicking on a date you can see a list of student's email id with their attendance percentage for that particular date.

## API routes:
- `{base_url}/api/login`
- `{base_url}/api/take-attendance`
- `{base_url}/api/attendance-response`
- `{base_url}/api/subscribe`