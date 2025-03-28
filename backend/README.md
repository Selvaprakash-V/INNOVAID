# JWT Authentication with MongoDB

Simple JWT Authentication API using Node.js, Express, MongoDB.

## 🚀 How to Run

1. Install dependencies:
```
npm install
```

2. Configure `.env` file with your MongoDB URI & JWT secret.

3. Run:
```
node app.js
```

4. Test:
- POST `/api/auth/signup`
- POST `/api/auth/login`
- GET `/api/auth/profile` (with token)
