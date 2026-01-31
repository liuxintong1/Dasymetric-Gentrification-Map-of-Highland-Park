# Highland Park Gentrification Map Visualization

Interactive map visualization showing gentrification data, zoning information, and commercial building prices for Highland Park, Los Angeles.

## 🚀 Deployment

**⚠️ Important**: This repository has restrictions. To deploy, **copy this project to your own GitHub repository** and follow the deployment guide.

See **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** for complete deployment instructions.

**Quick Summary**:
1. Fork or copy this repository to your own GitHub account
2. Update the base path in `.github/workflows/deploy.yml` with your repository name
3. Enable GitHub Pages in your repository settings
4. Your site will be deployed automatically!

---

## 🛠️ Tech Stack

- **Vue 3** - Frontend framework
- **Bootstrap 5.3.3** - UI styling and responsive design
- **Leaflet** - Interactive maps
- **D3.js** - Data visualization and SVG masking
- **Turf.js** - Spatial analysis

## 📦 Installation

```bash
npm install
```

## 🏃 Development

```bash
npm run dev
```

Runs the app in development mode at `http://localhost:3000`

## 🏗️ Build

```bash
npm run build
```

Builds the app for production to the `dist/` folder.

## 📄 Features

- **Interactive Map Layers**:
  - Toggleable zoning layer with gentrification-based color gradients
  - Gentrification tract outlines
  - Commercial building footprints with price colors

- **Color Encoding**:
  - Blue gradient for Single Family Residential zones
  - Purple gradient for Multifamily Residential zones
  - 5-level typology scale based on gentrification status

- **User Interface**:
  - Custom layer controls
  - Split legend layout (zoning on right, others on left)
  - Interactive popups with detailed information
  - Hover effects with outline highlighting

## 📝 Project Structure

```
project-team13/
├── src/
│   ├── components/
│   │   ├── GentrificationMap.vue      # Main map container
│   │   ├── ZoningLayer.vue            # Residential zones with gradients
│   │   ├── GentrificationTractsLayer.vue  # Tract outlines
│   │   ├── BuildingsWithPricesLayer.vue   # Commercial buildings
│   │   └── Legend.vue                 # Map legends
│   └── App.vue                        # Root component
├── public/                            # Static assets (GeoJSON files)
├── .github/workflows/
│   └── deploy.yml                     # GitHub Actions deployment
└── package.json                       # Dependencies

```

## 🔧 Configuration

- **Base Path**: Configured in `vite.config.js` via `VITE_BASE_PATH` environment variable
- **Build Output**: `dist/` directory
- **Deployment**: GitHub Actions workflow included (requires copying to your own repo)

## 📚 Documentation

- **DEPLOYMENT_GUIDE.md** - Complete deployment instructions
- See component files for detailed code documentation

## 📄 License

This project is part of a DSCI 554 course assignment.

