<script setup>
import GentrificationMap from './components/GentrificationMap.vue'
</script>

<template>
  <div id="app">
    <header>
      <h1>Highland Park, Los Angeles - Map Visualization</h1>
    </header>
    <GentrificationMap />
  </div>
</template>

<style scoped>
#app {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: Arial, sans-serif;
}

header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
  text-align: center;
}

header h1 {
  margin: 0;
  font-size: 1.5rem;
}
</style>