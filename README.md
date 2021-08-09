# django-channels-chat

## Introduction
A small functional Channels message center application built using Django - Channels. 
It has a paginated REST API to get the history of messages and django channels implementation with redis-channel layer for message communication.



## Installation Steps
### Step 1 - Install python dependencies
`pip install -r requirements.txt`

### Step 2 - Create database
`python manage.py makemigrations`

### Step 3 - Migrate database
`python manage.py migrate`

### Step 4 - Run Redis for channel layer
`docker run -p 6379:6379 -d redis:5`

### Step 5 - Install channels_redis so that Channels knows how to interface with Redi
`pip install channels_redis`

### Step 5 - Run the server
`python manage.py runserver`


## Running the project
Local Machine: 
host: http://localhost:8000

Heroku:
host: 

### Step 1 - Open Browser and login to django admin portal using by using following url 
http://localhost:8000/admin/

### Step 2 - Open Browsers incognito mode or different browser and login to django admin portal using by using following url 
http://localhost:8000/admin/

### Step 3 - Enter the room-name to join in the following url in both the windows. (In both the browsers)
http://localhost:8000/chat/

### Step 4 - Start typing the message in the newly opened site of the particular room.
http://localhost:8000/chat/<room_name>/

### Step 5 - Start typing the message in the newly opened site of the particular room in the other browser
http://localhost:8000/chat/<room_name>/

### Step 6 - Read Receipts will get updated if the message is read by the receipient. Reload the browser to see if the messages read by receipients.

### Step 7 - REST API is exposed to get the all the history of messages in a room.
http://localhost:8000/api/<room_name>/new/<page_no>
