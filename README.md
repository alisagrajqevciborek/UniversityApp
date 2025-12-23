# University App

Backend: Django + DRF; Frontend: React (basic scaffold provided).

Quick start (backend):

1. Create and activate venv: python -m venv venv; venv\Scripts\activate
2. Install dependencies: pip install -r requirements.txt
3. Run migrations: python manage.py migrate
4. Create sample data: python manage.py create_sample_data
5. Run server: python manage.py runserver

Auth:
- Obtain JWT token: POST /api/auth/token/ with {username, password}
- Use `Authorization: Bearer <token>` to access /api/dashboard/ and other endpoints

CORS:
- Currently restricted to `http://localhost:3000` for the React dev server. Modify `CORS_ALLOWED_ORIGINS` in `university/settings.py` when deploying.

Frontend:
- Recommended: run `npx create-react-app frontend`, then replace the generated `src/` with the provided `src/` files. Start with `npm start`.

Testing:
- Run `python manage.py test` to execute unit tests (they use the sqlite test DB).

Deployment notes:
- For PythonAnywhere (free tier), follow their guide to deploy Django apps. Ensure `ALLOWED_HOSTS` includes your pythonanywhere domain and set `DEBUG=False`.
