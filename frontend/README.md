# RecruitRankAI Vercel Frontend

This folder is a static Vercel-ready frontend for the FastAPI backend.

## Deploy

1. Deploy the backend first, for example on Render using `render.yaml`.
2. Deploy this `frontend/` folder to Vercel.
3. Paste the backend base URL into the UI, for example:

```text
https://recruitrankai-api.onrender.com
```

For a permanent default, edit `index.html` before `app.js` loads:

```html
<script>
  window.RECRUITRANKAI_API_BASE = "https://your-api.onrender.com";
</script>
```
