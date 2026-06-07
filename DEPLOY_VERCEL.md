# Deploying to Vercel

Deploy the React app and Vercel API functions as one Vercel project.

## Vercel Project

Create a Vercel project from the GitHub repository and set:

- Root Directory: `myfrontend`
- Framework Preset: `Create React App`
- Build Command: `npm run build`
- Output Directory: `build`

Add this Environment Variable in Vercel:

- `MONGODB_URI`: your MongoDB Atlas connection string

Do not set `REACT_APP_API_URL` for the Vercel deployment unless you are using a separate backend. Without it, the frontend calls the same-site API functions at `/api/register`, `/api/login`, and `/api/predict`.

After deployment, test:

```text
https://your-vercel-project.vercel.app/api/health
```

It should return:

```json
{"status": "ok"}
```

## Local Development

For local frontend development, the app still uses:

```text
http://127.0.0.1:5000
```

For local backend development, set `MONGODB_URI` before running Flask.
