# Smart O Class Backend
Taking and managing attendance in online classes made easy with chrome extensions. This repo contains code for the API endpoints required for the extension. It also contains code for the frontend website where-in user can see the attendance precentage of students inside a batch, date wise.

**Tech Stack-** Django, Django Rest Framework, SQLite3, HTML, CSS

## Project Setup Guide:
- Clone the repository
- After going into the required directory make a vitual environment and activate it.
- Run `pip install -r requirements.txt`  to install all the requirements/dependencies preferably setup a virtual environment and then do it. 
(**Note**- Your system must have python installed (version >= 3.7.6))
- You will have to run a migration to make the specific tables in the database so run the following command terminal:      
 `python manage.py migrate`        
- **Creating superuser**- This will give you the access to the admin page of the website. To make a superuser run `python manage.py createsuperuser` in the terminal and specify the details.
- Now you are good to go! Finally run `python manage.py runserver` or `python manage.py runserver <hostip>`to run the django application.

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

### Links to other parts of the project
- [https://github.com/ApoorvaRajBhadani/smartoclass-host](https://github.com/ApoorvaRajBhadani/smartoclass-host)
- [https://github.com/ApoorvaRajBhadani/smartoclass-attendee](https://github.com/ApoorvaRajBhadani/smartoclass-attendee)
- [https://github.com/ApoorvaRajBhadani/smartoclass-pushserver](https://github.com/ApoorvaRajBhadani/smartoclass-pushserver)


**Note-** For complete demo of the project refer to [link](https://www.youtube.com/watch?v=74c9yu5rTWc)