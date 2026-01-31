# Deployment Guide: Highland Park Map Visualization

This project uses **Vue.js with Bootstrap** and is ready for deployment. Since this repository has restrictions, you'll need to **copy this project to your own GitHub repository** to deploy it.

## ⚠️ Important: Copy to Your Own Repository

**You must copy this project to your own GitHub repository before deploying**, as this repository has restrictions on GitHub Actions.

---

## Quick Start: Deployment Steps

### Step 1: Copy the Project to Your Repository

**Option A: Fork the Repository (Recommended)**
1. Go to: https://github.com/DSCI-554/project-team13
2. Click the **"Fork"** button in the top-right corner
3. Select your personal GitHub account as the destination
4. Wait for the fork to complete

**Option B: Create New Repository and Push**
1. Create a new repository on GitHub (e.g., `highland-park-map`)
2. Clone this repository:
   ```bash
   git clone https://github.com/DSCI-554/project-team13.git
   cd project-team13
   ```
3. Remove the existing remote and add your own:
   ```bash
   git remote remove origin
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
   git push -u origin main
   ```

### Step 2: Update Configuration for Your Repository

After copying to your repository, you need to update the base path:

1. **Update `.github/workflows/deploy.yml`**:
   - Open `.github/workflows/deploy.yml`
   - Find the line: `VITE_BASE_PATH: '/project-team13/'`
   - Replace `project-team13` with **your repository name**
   - Example: If your repo is `highland-park-map`, change it to `VITE_BASE_PATH: '/highland-park-map/'`

2. **Commit the change**:
   ```bash
   git add .github/workflows/deploy.yml
   git commit -m "Update base path for deployment"
   git push origin main
   ```

### Step 3: Enable GitHub Pages

1. Go to your repository on GitHub: `https://github.com/YOUR-USERNAME/YOUR-REPO-NAME`
2. Click **Settings** → **Pages**
3. Under **Build and deployment** → **Source**, select **"GitHub Actions"**
4. Click **Save**

### Step 4: Wait for Deployment

1. Go to the **Actions** tab in your repository
2. You should see the "Deploy to GitHub Pages" workflow running
3. Wait 2-3 minutes for it to complete
4. Your site will be live at: `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/`

---

## Project Features

✅ **Vue 3** - Modern frontend framework  
✅ **Bootstrap 5.3.3** - Responsive UI components  
✅ **Leaflet** - Interactive maps  
✅ **D3.js** - Data visualization  
✅ **Turf.js** - Spatial analysis  
✅ **GitHub Actions** - Automatic deployment workflow  

---

## Configuration Files Included

- ✅ `.github/workflows/deploy.yml` - GitHub Actions deployment workflow
- ✅ `vite.config.js` - Configured for GitHub Pages deployment
- ✅ `src/main.js` - Bootstrap CSS imported
- ✅ `package.json` - All dependencies including Bootstrap

---

## Troubleshooting

### Assets Not Loading on GitHub Pages
- Ensure the base path in `.github/workflows/deploy.yml` matches your repository name
- Check that `vite.config.js` uses the `VITE_BASE_PATH` environment variable

### Build Fails
- Check the Actions tab for error logs
- Ensure all dependencies are in `package.json`
- Try building locally first: `npm run build`

### Repository Name Change
If you change your repository name, remember to:
1. Update `VITE_BASE_PATH` in `.github/workflows/deploy.yml`
2. Update the remote URL if needed: `git remote set-url origin NEW-URL`

---

## Expected Deployment URL Format

**GitHub Pages**: `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/`

---

## Summary Checklist

- [ ] Copy project to your own GitHub repository
- [ ] Update `VITE_BASE_PATH` in `.github/workflows/deploy.yml` with your repo name
- [ ] Enable GitHub Pages in repository Settings → Pages → GitHub Actions
- [ ] Push changes to trigger deployment
- [ ] Wait for deployment workflow to complete
- [ ] Access your live site at the GitHub Pages URL

**Happy Deploying! 🚀**

