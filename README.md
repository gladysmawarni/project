# cs50 final project 
# task-tracker web application
## link: https://tasktracker-py.herokuapp.com/
#### Video Demo:  https://youtu.be/nNE5sQyyfBA
#### Description:
For the final project, i decided to build a web application using Flask, Python, HTML, CSS, and JavaScript.
I wrote the code in Visual Studio Code and i am using SQLalchemy and postgresql to manage the database.
The purpose of the web app is to keep track of the task that one's need to be done.

### register
The first page that i made is the registration page, to allow users to use the app individually and privately. By creating a table containing user id, username, and (hashed) password,
anyone with a unique username can have their own homepage and create their own entries of to-do tasks.
The registration page consists of a form of 3 fields for username, password, and password confirmation to make sure the user is entering the password they meant.
By clicking the "register" button the data will be recorded in the database.
After completing the form, the user is taken to their own homepage.

![image](https://user-images.githubusercontent.com/78975611/160450049-c85aa2d0-db23-441c-9351-aa960fb16ff4.png)



### login
After the registration page, i build the login page for returning users. The log in page consists of a form of 2 fields, for username and password.
If the username is not registered or the password is not correct, a message will be shown to inform the user.
I used the flask_session to keep track of the logged user.

![image](https://user-images.githubusercontent.com/78975611/155982061-f16ea72d-e0eb-4b89-bb7b-e8f077473582.png)


### index/homepage
In the homepage, there will be a greeting based on the user's time (Good Morning, Good Afternoon, or Good Evening), followed by the logged-in user's username.
It will also shows the date for today.
I was considering to include the weather widget in the homepage, but it turns out locating the user's location and make a decent weather widget is harder than i tought,
so i will have to put off the idea for now and hopefully make it in the future.
In the homepage, there's 2 button.
The first one is to create a new entry, when it is clicked, a modal form will appear. The form will prompt user for the task's name, description, and the deadline.
To keep track of the entries, i created a table containing the entry id, user id, title, description, deadline, finished(boolean), and finished date.
After clicking "create", the data will be recorded in the database and
the entry will now appear in the homepage. The entries is ordered by the tasks with the closest deadline first.
When the task is completed, the user can click the "finished" button on the specific entry to move it to the history page. The button will trigger the finished boolean value to True,
so I can filter out the finished task.
The second button is to go to the history's page.

![image](https://user-images.githubusercontent.com/78975611/155981906-014001b0-cdcb-4b41-ab80-8b4278ec2b25.png)


### history
In the history page, the users can see the tasks that they had completed. It is also shown the date of when the task is finished (when the "finished" button is clicked).
To go back to the homepage / to see the tasks that still need to be done, the user can click the "see all entries" button.

### logout
When the user is done, they can log out by simply clicking the "Log Out" button on the upper right corner of the website. Which will just clear the session.
