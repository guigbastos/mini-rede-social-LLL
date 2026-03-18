<div align="right">
  <a href="https://github.com/guigbastos/mini-rede-social-LLL/blob/main/README-en.md">
    <img alt="English" src="https://img.shields.io/badge/English-blue?style=for-the-badge&logo=us">
  </a>
  <a href="https://github.com/guigbastos/mini-rede-social-LLL/blob/main/README.md">
    <img alt="Português" src="https://img.shields.io/badge/Português-green?style=for-the-badge&logo=br">
  </a>
</div>

---

# 📱 Mini Social Network API

A robust RESTful API for a social network, developed with Python and Flask. This project focuses on Software Engineering best practices, including Clean Code, layered architecture pattern (Controller, Service, Repository), and data security.

## 🚀 Features

* **Authentication and Security:**
  * User creation with encrypted passwords (Hash).
  * Secure login with JWT (JSON Web Tokens) generation.
  * Protected routes requiring authentication.

* **Post Management:**
  * Full CRUD for posts.
  * Logical deletion (*Soft Delete*) to maintain database integrity.

* **Social Interactions:**
  * **Follower System:** Self-referential relationship (many-to-many) allowing users to follow and unfollow each other.
  * **Like System:** Relationship (many-to-many) between users and posts.
  * **Custom Feed:** Advanced data crossing via relational database (Subqueries/JOINs) to deliver an exclusive feed containing only posts from users the person follows.

## 🛠️ Technologies Used

* **Language:** Python 3
* **Framework Web:** Flask
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Authentication:** Flask-JWT-Extended

## ⚙️ How to run the project locally

### Prerequisites
Make sure you have [Python 3](https://www.python.org/) and [PostgreSQL](https://www.postgresql.org/) installed on your machine.

### Step-by-step

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/guigbastos/mini-rede-social-LLL.git](https://github.com/guigbastos/mini-rede-social-LLL.git)
   cd mini_rede_social

2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt

4. **Configure environment variables:**
   - Create a file named `.env` in the project root by copying the template.
   - Fill in your PostgreSQL database details and create your secret keys.

5. **Start the server:**
    ```bash
    python run.py

<!-- The API will be running at http://127.0.0.1:5000/ -->

## 🛣️ Roadmap

### 🛡️ Security, Access & Moderation (RBAC)
- [X] **Privilege Escalation:** API interface for Administrators to manage and change user *roles* (e.g., Promote to Moderator).
- [X] **Account Moderation:** Endpoint for Moderators to apply blocks or suspensions on offending accounts.
- [X] **State Validation (Account Lockout):** Strict business rule to prevent post creation or interactions by blocked accounts.

### ⚙️ Administrative Management (Backoffice)
- [X] **Central User Management (Admin):** Full CRUD (Creation, Editing, and Soft/Hard Delete) for total control over user records.
- [ ] **Reporting System (Complaints):** Workflow for users to report posts and accounts that violate community guidelines.

### 📝 Content & Social Engagement
- [X] **Content Update:** Endpoint (`PUT/PATCH`) allowing authors to modify the text of already published posts.
- [ ] **Engagement Metrics:** Optimized system for counting likes per post.
- [ ] **Connection Metrics:** Optimized system for counting "Followers" and "Following" on user profiles.

### 🚦 Stability & Abuse Prevention
- [ ] **Rate Limiting (Anti-Spam):** Programmed limitation of request volume for posts to avoid *flooding* and database overload.

### 🌐 Ecosystem & Integration
- [ ] **Client Application (Front-end):** Development of an interactive graphical interface (SPA) for full consumption and integration with the REST API.