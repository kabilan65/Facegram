# Facegram

Facegram is a social media web application inspired by Instagram. It allows users to share posts, interact with others, and personalize their profiles. Built using Django, Facegram demonstrates the power of Python in creating dynamic and responsive web applications.

## Features

- **User Authentication**: 
  - Register, login, and logout functionality.

- **User Profile**:
  - View and update user profiles, including bio, profile picture, and location.

- **Posts**:
  - Upload posts with photos.
  - Delete posts created by the user.
  - Like and unlike posts.
  - View posts you haven't liked yet.

- **Comments**:
  - Add comments to posts.

- **Follow/Unfollow**:
  - Follow and unfollow other users.
  - View followers and following counts.

- **User Suggestions**:
  - Get user suggestions based on people you don't follow.

- **Search Functionality**:
  - Search for users by username.

- **Post Feed**:
  - A feed showing posts from users you follow.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kabilan65/Facegram.git
   cd Facegram

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   pip install -r requirements.txt

3. Apply migrations:
   python manage.py makemigrations
   python manage.py migrate

4. Run the development server:
   python manage.py runserver

5. Open the application in your browser:
   Navigate to http://127.0.0.1:8000
