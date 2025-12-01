# Quick Start: Copy & Deploy

## ⚠️ Repository Restrictions Notice

**This repository has restrictions that prevent using GitHub Actions directly.**

You must **copy this project to your own GitHub repository** before deploying.

---

## 🚀 3-Step Deployment

### Step 1: Copy to Your Repository

**Fork this repository:**
1. Go to: https://github.com/DSCI-554/project-team13
2. Click **"Fork"** button → Select your account
3. Or create a new repository and push this code to it

### Step 2: Update Repository Name in Config

Edit `.github/workflows/deploy.yml`:
- Find line 40: `VITE_BASE_PATH: '/project-team13/'`
- Change `project-team13` to **your repository name**
- Commit and push the change

### Step 3: Enable GitHub Pages

1. Go to your repository → **Settings** → **Pages**
2. Under **Source**, select **"GitHub Actions"**
3. Click **Save**
4. Check **Actions** tab - deployment will run automatically

**Your site will be live at**: `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/`

---

## 📦 What's Included

✅ **Vue 3** with **Bootstrap 5.3.3**  
✅ **GitHub Actions** deployment workflow  
✅ **Complete configuration** ready to use  

---

## 📖 Full Instructions

See **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** for detailed steps and troubleshooting.

---

## 🆘 Need Help?

- Check deployment workflow logs in the **Actions** tab
- Verify base path matches your repository name
- See DEPLOYMENT_GUIDE.md for troubleshooting tips

