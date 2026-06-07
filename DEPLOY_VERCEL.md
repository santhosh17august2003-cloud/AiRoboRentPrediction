# Deploying to Vercel

Deploy this repository as two Vercel projects.

## 1. Backend

Create a new Vercel project from the same GitHub repository and set:

- Root Directory: `mybackend`
- Framework Preset: `Other`
- Build Command: leave empty
- Output Directory: leave empty

Add this Environment Variable in Vercel:

- `MONGODB_URI`: your MongoDB Atlas connection string

After deployment, copy the backend URL, for example:

```text
https://your-backend-project.vercel.app
```

## 2. Frontend

Create another Vercel project from the same GitHub repository and set:

- Root Directory: `myfrontend`
- Framework Preset: `Create React App`
- Build Command: `npm run build`
- Output Directory: `build`

Add this Environment Variable in Vercel:

- `REACT_APP_API_URL`: the backend URL from step 1

Redeploy the frontend after adding `REACT_APP_API_URL`.

## Local Development

For local frontend development, the app still uses:

```text
http://127.0.0.1:5000
```

For local backend development, set `MONGODB_URI` before running Flask.
