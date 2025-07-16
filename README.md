# 4-6_Work_with_MongoDB

# 🚀 Archive Inactive Users

Automates archiving of inactive users from a MongoDB database.

## 📋 Task Overview

- Identify users:
  - Registered more than 30 days ago  
  - No activity in the last 14 days  
- Move them to `archived_users` collection  
- Generate daily JSON report (`YYYY-MM-DD.json`) summarizing archive count and user IDs

> Manual execution — no cron or scheduling.

---

## 🛠️ Setup & Usage

1. **Clone the repo**

   ```bash
   git clone https://github.com/your-org/archive-inactive-users.git
   cd archive-inactive-users

2. **Configure MongoDB**
- Defaults to mongodb://localhost:27017/
- Database: my_database
- Collections: user_events, archived_users
- Run the script

3. **Run the script**

   ```bash
   python3 archive_inactive_users.py

**Outputs:**

- Moves qualifying users to archived_users
- Writes report file named YYYY-MM-DD.json, e.g. 2025-03-30.json

## 🧠 How It Works
1. Calculate cutoffs:
- registration_cutoff = today − 30 days
- activity_cutoff = today − 14 days

2. Aggregate user_events to get:
- Last event time per user
- Registration date and email

3. Filter users:
- registration_date < registration_cutoff
- last_event < activity_cutoff

4. Archive users:
- Insert records into archived_users
- Log user_id, email, registration and last activity timestamps, plus archived_at

5. Generate JSON report:

   ```bash
   {
   "date": "2025-03-30",
   "archived_users_count": 3,
   "archived_user_ids": [123, 456, 789
   }
## 📦 Report Format
Filename: YYYY-MM-DD.json

Example:

   ```bash
   {
   "date": "2025-03-30",
   "archived_users_count": 3,
   "archived_user_ids": [123, 456, 789]
   }

