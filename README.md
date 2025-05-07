See project description for setup and deployment instructions.
# 📅 OnCall Scheduler Web Application

A simple and automated OnCall Scheduler built using:

- **AWS CDK** → Infrastructure as Code (DynamoDB + Lambda + EventBridge)
- **Elastic Beanstalk** → Flask-based Web UI and API
- **DynamoDB** → To store Users and OnCall Schedules
- **Lambda + EventBridge** → To automatically rotate OnCall every week

---

## 🚀 Features

✅ Add / Remove OnCall users via REST API  
✅ View Current OnCall User on Web UI  
✅ Automatically rotate OnCall user every Monday  
✅ Simple UI built using Flask and HTML  
✅ Powered by serverless architecture using AWS services

---

## 📦 Project Structure

```
oncall_scheduler_project/
├── cdk/               # AWS CDK (DynamoDB, Lambda, EventBridge)
├── webapp/            # Elastic Beanstalk Flask application
│   ├── application.py # Flask app (Web UI + Users API)
│   ├── requirements.txt
│   └── templates/
│       └── index.html
└── README.md
```

---

## 🛠️ Setup & Deployment

### 1️⃣ Deploy AWS Resources using CDK

```bash
cd cdk
cdk bootstrap
cdk deploy
```

✅ Creates DynamoDB tables → OnCallUsers + OnCallSchedule  
✅ Creates Lambda → OnCallRotationLambda  
✅ Creates EventBridge Rule → Weekly trigger for Lambda

---

### 2️⃣ Deploy Web App using Elastic Beanstalk

```bash
cd webapp
eb init -p python-3.10 oncall-scheduler --region us-west-2
eb create oncall-scheduler-env
```

✅ Flask application will be deployed and publicly accessible

---

### 3️⃣ Configure Environment Variables

```bash
eb setenv USERS_TABLE=<DynamoDB Users Table Name> SCHEDULE_TABLE=<DynamoDB Schedule Table Name>
```

---

### 4️⃣ Add OnCall Users

```bash
curl -X POST http://<EB-URL>/users -H "Content-Type: application/json" -d '{"id": "user1", "name": "Arun", "email": "arun@example.com"}'
curl -X POST http://<EB-URL>/users -H "Content-Type: application/json" -d '{"id": "user2", "name": "John", "email": "john@example.com"}'
```

✅ Adds users into DynamoDB

---

### 5️⃣ View Current OnCall User

Visit your Elastic Beanstalk Web URL:

```
http://oncall-scheduler-env.eba-xxxxxxx.us-west-2.elasticbeanstalk.com/
```

✅ Displays current OnCall user (if schedule populated)

---

### 6️⃣ Trigger Weekly Rotation (optional manual trigger)

Run Lambda manually for first time (in AWS Console → Lambda → OnCallRotationLambda → Test).

✅ Populates OnCallSchedule DynamoDB table

✅ Webpage will now show → Current OnCall User

✅ Future rotations → automatic every Monday

---

## 📊 API Endpoints

| Method | URL            | Description       |
|--------|----------------|-------------------|
| GET    | /users         | List all users    |
| POST   | /users         | Add new user      |
| DELETE | /users         | Delete user       |
| GET    | /              | Current OnCall UI |

---

## ✅ Final Status

✔️ Users API → Working  
✔️ Schedule → Populated  
✔️ OnCall Rotation → Automatic + Manual (Lambda)  
✔️ Web UI → Displays current OnCall  
✔️ Deployment → Elastic Beanstalk → ✅ LIVE
✔️ Email notifications to OnCall user

---

## 📌 Optional Future Enhancements


- Admin UI to manage users/schedules
- UI design enhancement (Bootstrap, etc)
- Slack or Teams integration

---

## 📢 Author

Arun Yalate
