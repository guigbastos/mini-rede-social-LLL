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
  * 280-character limit enforced on both creation and update.

* **Social Interactions:**
  * **Follower System:** Self-referential relationship (many-to-many) allowing users to follow and unfollow each other.
  * **Like System:** Relationship (many-to-many) between users and posts.
  * **Custom Feed:** Advanced data crossing via relational database (Subqueries/JOINs) to deliver an exclusive feed containing only posts from users the person follows.
  * **Public Profile:** Profile endpoint with connection metrics (followers and following counts).

* **Moderation and Access Control (RBAC):**
  * Three role levels: User, Moderator, and Administrator.
  * Account blocking with toggle support (block/unblock).
  * Moderator promotion and demotion by the Administrator.
  * Blocked accounts are prevented from posting, liking, retweeting, and commenting.

* **Reporting System:**
  * Users can report posts and other users.
  * Moderators and Admins manage reports through a dedicated panel.
  * Status flow: `pending` → `reviewed` / `dismissed`.

* **Abuse Prevention:**
  * Rate Limiting on post creation (10 per minute per IP).
  * Protection against duplicate reports and self-reports.

## 🛠️ Technologies Used

* **Language:** Python 3
* **Web Framework:** Flask
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Authentication:** Flask-JWT-Extended
* **Rate Limiting:** Flask-Limiter
* **Documentation:** Flasgger (Swagger UI)

## ⚙️ How to run the project locally

### Prerequisites
Make sure you have [Python 3](https://www.python.org/) and [PostgreSQL](https://www.postgresql.org/) installed on your machine.

### Step-by-step

1. **Clone the repository:**
   ```bash
   git clone https://github.com/guigbastos/mini-rede-social-LLL.git
   cd mini_rede_social
   ```

2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables:**
   - Create a file named `.env` in the project root by copying the template.
   - Fill in your PostgreSQL database details and create your secret keys.

5. **Start the server:**
    ```bash
    python run.py
    ```

<!-- The API will be running at http://127.0.0.1:5000/ -->
<!-- Interactive documentation will be available at http://127.0.0.1:5000/apidocs/ -->

## 🛣️ Roadmap

### 🛡️ Security, Access & Moderation (RBAC)
- [X] **Privilege Escalation:** API interface for Administrators to manage and change user *roles* (e.g., Promote to Moderator).
- [X] **Account Moderation:** Endpoint for Moderators to apply blocks or suspensions on offending accounts, with toggle support (block/unblock).
- [X] **State Validation (Account Lockout):** Strict business rule to prevent post creation, likes, retweets, and comments by blocked accounts.

### ⚙️ Administrative Management (Backoffice)
- [X] **Central User Management (Admin):** Full CRUD (Creation, Editing, and Soft/Hard Delete) for total control over user records.
- [X] **Reporting System (Complaints):** Complete workflow for users to report posts and accounts. Moderators and Admins review reports via a dedicated panel with `resolve` and `dismiss` actions.

### 📝 Content & Social Engagement
- [X] **Content Update:** Endpoint (`PUT`) allowing authors to modify the text of already published posts.
- [X] **Engagement Metrics:** Like counter per post embedded in every post response (`likes_count`).
- [X] **Connection Metrics:** Follower and following counts available on the profile route (`GET /users/<id>/profile`) and on listing routes (`GET /users/<id>/followers` and `/following`).

### 🚦 Stability & Abuse Prevention
- [X] **Rate Limiting (Anti-Spam):** Limit of 10 posts per minute per IP via Flask-Limiter, with a standardized HTTP 429 response.

### 🌐 Ecosystem & Integration
- [ ] **Client Application (Front-end):** Development of an interactive graphical interface (SPA) for full consumption and integration with the REST API.