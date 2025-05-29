<template>
  <header id="header">
    <h1>
      Simple News!
    </h1>
    <Navbar />
  </header>

  <main>
    <RouterView />
  </main>

  <footer>
    <p>© {{ year }} Simple News! - build with ❤️ with VueJs</p>
  </footer>

</template>
<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'

const year = new Date().getFullYear();
</script>

<style scoped></style>
