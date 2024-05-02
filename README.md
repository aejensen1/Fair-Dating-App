# Fair-Dating-App

Project that demonstrates an understanding of how to create, configure, and manage a database.

This project was alloted a timespan of approximately 2 weeks, so I decided to keep the framework simple by leveraging Flask with an html, css, and javascript front end. MongoDB was the database of choice, as a short amount of research indicated this nosql option is widely adopted by dating apps due to its great flexibility and scalability.

User authentication is overall complete, using Flask's provided flask_login and LoginManager libraries. A user cannot login until a username and password is added to the database. Passwords are hashed before saving to the database to promote security. Once a user authenticates in, they can then access the other protected directories. The user cannot swipe on others until their profile is completed. 

In the edit-profile route, the user must enter all required fields, including an image and birthday, which is checked to ensure the user is over 18 years old. After all fields are complete the user can submit and the data is saved to their user document in the Users collection of the database. If the user chooses to edit their profile again, the information stored in the database will automatically be pulled and populate the fields.

Now the user can see other users on the home page. Random user profiles that are complete will show every time the page is refreshed. The backend will skip a random number of users that have their profile marked as complete and then forward that data to the html template to be displayed.

All in all, this program demonstrates knowledge in how to create, add to, update, and get information from a database. I plan to use these concepts to make a new version of this data app using React Native, so that the app itself is more versatile and scalable. It can then be pushed to mobile applications.
