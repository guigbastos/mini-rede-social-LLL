# Social Network API Documentation

[🇧🇷 Leia em Português](./API_pt-BR.md)

This documentation describes the available endpoints for the Social Network API.

## 🔒 Authentication
Most routes require JWT (JSON Web Token) authentication.
The token must be sent in the request Header in the following format:
`Authorization: Bearer <your_token_here>`

---

## 👥 Users

### 1. Register New User
Creates a new account on the platform.

- **URL:** `/users/register`
- **Method:** `POST`
- **Auth Required:** No

**Request Body:**
```json
{
  "username": "your name here",
  "email": "your mail address here",
  "password": "secure_password123"
}
```

**Success Response (201 CREATED):**
```json
{
  "message": "User created successfully!"
}
```

**Error Response (400 BAD REQUEST):**
```json
{
  "error": "This email is already in use."
}
```