import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Project Pages live at /<repo>/; keep local `vite` / `vite preview` at `/`.
const repoName = process.env.GITHUB_REPOSITORY?.split('/')[1]
const isUserSite = repoName?.endsWith('.github.io')
const inferredBase = repoName && !isUserSite ? `/${repoName}/` : '/'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: process.env.VITE_BASE_PATH || inferredBase,
  server: {
    port: 3000,
    open: true
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  }
})