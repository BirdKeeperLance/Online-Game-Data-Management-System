# Online-Game-Data-Management-System
There's a lot of data to be found in games, from basic information like player name, date of joining, player level to advanced ever changing data like ranking, battle logs and matchmaking opponents. This project aims to use MongoDB, Flask and basic HTML and CSS to display the information. 

**Technologies Used:**

Flask: Python web framework for building the backend application.

MongoDB: NoSQL database used for storing game-related data such as users, player profiles, rankings, battle logs, and reports.

HTML/CSS: Used for frontend templates and styling.

Python Libraries: Including Flask, pymongo for MongoDB interaction, and bson for ObjectId handling.

**Features:**

**User Authentication:**

Users can sign up with a username and password.
Existing users are prevented from signing up again.
Upon successful sign-in, users are redirected to their respective dashboards based on their role (ADMIN, MODERATOR, PLAYER).
Role-based Dashboards:

**Admin Dashboard:**

Accessible only to users with the role 'ADMIN'.
Displays lists of players, rankings, battle logs, and moderators.
Admins can view reports filed by moderators and take actions such as deleting players, changing rankings, and deleting moderators.

**Moderator Dashboard:**

Accessible only to users with the role 'MODERATOR'.
Provides access to player-related data including rankings and battle logs.
Moderators can report players, which are then viewable by admins for further action.

**Player Dashboard:**

Accessible to users with the role 'PLAYER'.
Shows the player's profile information, current ranking, and battle history.

**Reporting System:**

**Moderator Reporting:**

Moderators can report players with reasons specified.
Reports are stored in MongoDB and can be viewed by admins for review and action.

**Data Management:**

**Player Management:**

New players can be created by using the signup page, this creates a new document in the MongoDB database and the player is given an initial level of 1.
Admins can delete players, which removes associated data such as rankings and battle logs.

**Moderator Management:**

Admins can delete moderators from the system.

**Ranking Management:**

Admins can change a player's ranking, updating the MongoDB collection accordingly.

**Session Management:**

Uses Flask's session management for storing user information securely during their session.

**Error Handling:**

Basic error handling for invalid credentials and unauthorized access to certain routes.

**Project Structure:**

app.py: Main application file containing route definitions, MongoDB connections, and route handlers for various functionalities.
Templates: HTML files for rendering different dashboard views and forms.
