# -Veterinary-Clinic---Python-GUI-Project
Python desktop application for managing owners and pets in a veterinary clinic. Includes a user-friendly GUI, local SQLite database, and automated email reminders for expired vaccinations

## 🐾 Features

### For Veterinarians:
- Add new pet owners (name, surname, email, phone)
- Add new pets (name, species, age, owner ID, vaccination date)
- View list of all pet owners
- Update vaccination date for pets
- Check expired vaccinations and automatically send email reminders to owners

### For Pet Owners:
- View a list of their pets by entering their owner ID

## 🛠 Technologies Used

- **Python 3**
- **Tkinter** - for building the GUI
- **SQLite** - local database for storing owners and pets
- **tkcalendar** - date picker widget for vaccination dates
- **smtplib** - for sending automated email reminders

## 🗄 Database

The application uses a local SQLite database (`database.db`) with two tables:
- `owners` - stores information about pet owners
- `pets` - stores information about pets, including vaccination dates and foreign key to owner

## ✉️ Email Notifications

When a pet's vaccination date has expired (more than 1 year old), the application can:
- Identify expired vaccinations
- Automatically send an email reminder to the owner's registered email address

**Note:** You need to provide valid email credentials in the code for the email functionality to work.

## 🚀 How to Run the Application

1. Clone the repository:
   
```bash
git clone https://github.com/AnitaCloudTech/veterinary-clinic-python-gui-project.git
cd veterinary-clinic-python-gui-project

```
2. Install dependencies:
   
```bash

pip install -r requirements.txt

```
3. Run the application:

```bash

python main.py

```

The application will open a graphical interface where you can choose to operate as a veterinarian or a pet owner.

## ⚠️ Important Notes

- The database (`database.db`) is created automatically if it does not exist.
- Email functionality uses Gmail SMTP - you need to allow **Less Secure Apps** or generate an **App Password** if using Gmail.
- For demonstration purposes, the application sends emails directly from the code using hardcoded credentials. **In production, never store credentials in code.**

## 💡 Potential Improvements

- Store email credentials securely (environment variables or config files)
- Add password authentication for veterinarian access
- Improve user interface layout
- Export reports (PDF/CSV) of pets and owners
- Dockerize the application for easier deployment

## 📁 Project Structure

```plaintext
veterinary-clinic/
│
├── main.py # Main application code
├── database.db # Local SQLite database (created automatically)
├── requirements.txt # List of required Python packages
└── .gitignore # Files excluded from version control

