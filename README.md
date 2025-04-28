#-> e-Register
e-Register is a web application for managing and submitting student activities. It allows users (students and admin) to register their activities, view previously submitted notes, and manage them easily. The system includes a feature for creating, editing, and deleting notes, providing a user-friendly interface for students and administrators.

------------------------------------------------------------------------------------------------------------------

#-> Features\


@For Admin:
Login/Logout: Secure admin login to manage the platform.

Create Notes: Admins can post daily highlights or updates for the college students.

View All Notes: Admin can see all the submitted notices of students.

Edit/Delete Notes: Modify or delete previously submitted activities.


@For Students:
Login/Logout: Secure student login to submit activities.

Create Notes: Student can't create notice as misuse can happen.

View My Notes: View personal warning in a personal list.



@Shared Features:
User Profile: Users can view their profile, change their password, and log out.

Responsive Design: The app is designed to be mobile-friendly with a modern UI.

------------------------------------------------------------------------------------------------------------------

#-> Technologies Used


@Backend: FastAPI

@Frontend: HTML, CSS, JavaScript, Bootstrap 5

@Database: MongoDB (used for storing user data and activity notes)

@Authentication: Session-based user login

@Libraries/Tools:

SweetAlert2 (for notifications)

FontAwesome (for icons)

------------------------------------------------------------------------------------------------------------------

#-> Installation Guide


Prerequisites:

Python 3.7 or later

MongoDB account and a cluster (free tier is fine)

------------------------------------------------------------------------------------------------------------------


#-> Steps:
1.Clone the repository:

git clone https://github.com/ayush-5158/e-register.git
cd e-register


2.Set up a virtual environment (optional but recommended):

python -m venv venv
On macOS/Linux: source venv/bin/activate  
On Windows: venv\Scripts\activate


3.Install dependencies:
pip install -r requirements.txt


4.Set up MongoDB:

Create a free MongoDB cluster at MongoDB Atlas.

Get your connection string and replace the MONGO_URI in your FastAPI configuration file.

5.Run the application:


uvicorn index:app --reload
The app will be live on http://localhost:8000.

------------------------------------------------------------------------------------------------------------------
#-> Usage


@Login Page:

Use the login form to either sign in as a student or admin.

@Dashboard:

Once logged in, users will be redirected to the dashboard where they can create, view, edit, or delete notes.

Admin users can also post updates and view all notes submitted by students.

@User Profile:

Click the dropdown in the top right corner to access the user profile, change your password, or log out.

------------------------------------------------------------------------------------------------------------------

#-> File Structure

e-register/
│
├── app/
│   ├── main.py                 # FastAPI app and routing
│   ├── models.py               # MongoDB models
│   ├── templates/              # Jinja2 HTML templates
│   ├── static/                 # Static files (CSS, JS, images)
│   ├── routes/                 # Route files for specific functionality (e.g., note handling)
│
├── requirements.txt            # Python dependencies
├── README.md                  # Project documentation

------------------------------------------------------------------------------------------------------------------

License
This project is licensed under the MIT License - see the LICENSE file for details.

