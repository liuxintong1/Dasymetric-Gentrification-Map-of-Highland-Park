<template>
  <div id="app">
    <nav class="main-nav">
      <div class="nav-brand">
        <h1>LA Gentrification Analysis</h1>
      </div>
      <div class="nav-links">
        <router-link to="/gentrification" class="nav-link">
          Temporal Map
        </router-link>
        <router-link to="/neighborhood" class="nav-link">
          Neighborhood Analysis
        </router-link>
        <router-link to="/migration" class="nav-link">
          Migration Flow
        </router-link>
      </div>
    </nav>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
// No changes needed here
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.main-nav {
  background: #2c3e50;
  color: white;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.nav-brand h1 {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background 0.2s;
  font-weight: 500;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
}

.nav-link.router-link-active {
  background: #3182bd;
}

.main-content {
  flex: 1;
  overflow: hidden;
  position: relative;
}
</style>
