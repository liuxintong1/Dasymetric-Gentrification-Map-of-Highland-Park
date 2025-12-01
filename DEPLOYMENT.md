# Deployment Guide: GitHub Pages

This guide explains how to deploy the Highland Park Map Visualization to GitHub Pages.

## Prerequisites

- GitHub account
- Repository: `DSCI-554/project-team13`
- Node.js and npm installed locally

## Deployment URL

Once deployed, your app will be available at:
**https://dsci-554.github.io/project-team13/**

---

## Automatic Deployment (Recommended)

The project includes a GitHub Actions workflow that automatically deploys on every push to the `main` branch.

### Steps:

1. **Enable GitHub Pages in Repository Settings**
   - Go to your repository: https://github.com/DSCI-554/project-team13
   - Click **Settings** → **Pages**
   - Under **Source**, select **GitHub Actions**
   - Save the changes

2. **Push Your Code**
   - The deployment workflow (`.github/workflows/deploy.yml`) is already configured
   - Simply push your changes to the `main` branch:
   ```bash
   git add .
   git commit -m "Setup GitHub Pages deployment"
   git push origin main
   ```

3. **Monitor Deployment**
   - Go to **Actions** tab in your repository
   - Watch the deployment workflow run
   - Once complete, your site will be live at the URL above

---

## Manual Deployment (Alternative)

If you prefer to deploy manually:

1. **Build the project locally:**
   ```bash
   npm install
   npm run build
   ```

2. **Deploy the `dist` folder:**
   - Go to repository **Settings** → **Pages**
   - Select **Deploy from a branch**
   - Choose branch: `gh-pages` (or create it)
   - Select folder: `/dist`

3. **Create and push gh-pages branch:**
   ```bash
   git checkout --orphan gh-pages
   git rm -rf .
   cp -r dist/* .
   git add .
   git commit -m "Deploy to GitHub Pages"
   git push origin gh-pages
   ```

---

## Configuration Details

### Base Path
The `vite.config.js` is configured with base path `/project-team13/` for production builds. This ensures all assets load correctly on GitHub Pages.

### Build Output
- Build directory: `dist/`
- Assets directory: `dist/assets/`
- All static files from `public/` are copied to `dist/`

---

## Troubleshooting

### Assets Not Loading
- Verify the base path in `vite.config.js` matches your repository name
- Check that paths in your code use relative paths, not absolute paths

### 404 Errors
- Ensure GitHub Pages is enabled in repository settings
- Check that the deployment workflow completed successfully
- Verify the base path configuration

### Styling Issues
- Clear browser cache
- Check browser console for asset loading errors
- Verify Bootstrap CSS is imported in `main.js`

---

## Project Features

✅ **Vue 3** - Modern frontend framework  
✅ **Bootstrap 5** - Responsive UI components  
✅ **Leaflet** - Interactive maps  
✅ **D3.js** - Data visualization  
✅ **Turf.js** - Spatial analysis  
✅ **GitHub Actions** - Automatic deployment  

---

## Repository Structure

```
project-team13/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions deployment workflow
├── public/                     # Static assets (GeoJSON files)
├── src/                        # Vue components
├── vite.config.js             # Vite configuration with base path
└── package.json               # Dependencies including Bootstrap
```

---

## Need Help?

- Check GitHub Actions logs in the **Actions** tab
- Verify repository settings in **Settings** → **Pages**
- Review the deployment workflow file: `.github/workflows/deploy.yml`

