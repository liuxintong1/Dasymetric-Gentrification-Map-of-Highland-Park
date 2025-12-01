# Quick Start: Deploy to GitHub Pages

## 🚀 Quick Steps

### 1. Enable GitHub Pages
Go to: https://github.com/DSCI-554/project-team13/settings/pages
- Under **Source**, select **GitHub Actions**
- Save

### 2. Push Your Code
```bash
git add .
git commit -m "Setup GitHub Pages deployment with Bootstrap"
git push origin main
```

### 3. Wait for Deployment
- Go to **Actions** tab: https://github.com/DSCI-554/project-team13/actions
- Wait for workflow to complete (usually 2-3 minutes)

### 4. Your Site is Live! 🎉
**URL:** https://dsci-554.github.io/project-team13/

---

## What Was Set Up

✅ **Vite Configuration** - Base path set to `/project-team13/`  
✅ **GitHub Actions Workflow** - Automatic deployment on push  
✅ **Bootstrap 5.3.3** - Added and imported  
✅ **Build Configuration** - Optimized for production  

---

## Files Changed

- `vite.config.js` - Added base path for GitHub Pages
- `src/main.js` - Added Bootstrap CSS import
- `.github/workflows/deploy.yml` - Created deployment workflow
- `package.json` - Added Bootstrap dependency

---

## Need More Details?

See `DEPLOYMENT.md` for comprehensive deployment guide.

