# Schedule Tracker

A simple and elegant web application for tracking tasks, managing priorities, and maintaining focus using a built-in timer.

## Features

- Task Management (Add, Update, Delete)
- Priority Settings (High, Medium, Low)
- Focus Timer with Sound Alert
- Performance Tracking
- Modern and Responsive UI

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

### Task Management
- Add new tasks with title, description, priority, and due date
- Edit existing tasks by clicking the "Edit" button
- Delete tasks using the "Delete" button
- Mark tasks as complete to increase your performance score

### Focus Timer
- Set a timer duration (1-60 minutes)
- Start/Reset the timer as needed
- Receive an audio alert when the timer ends

### Performance Tracking
- Complete tasks to increase your performance score
- Score calculation uses a diminishing returns formula
- Track your total completed tasks

## Technologies Used

- Python
- Flask
- SQLite
- Bootstrap 5
- JavaScript

## Project Structure

```
schedule_tracker/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── static/
│   ├── style.css      # Custom styles
│   └── script.js      # JavaScript functionality
├── templates/
│   └── index.html     # Main template
└── README.md          # This file
``` 