Quick frontend setup

Prefer using create-react-app for an easy setup:

1) From project root run: npx create-react-app frontend
2) Replace the generated `src/` files with the provided `src/` files in this repo (Login, Dashboard, index.js, styles.css)
3) Run `npm start` (default port 3000)

The React app will talk to the API at http://127.0.0.1:8000 (CORS is configured to allow localhost:3000). The login hints (admin/adminpass etc) are seeded by the management command `create_sample_data`.