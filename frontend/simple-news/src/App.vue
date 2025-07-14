<template>
  <header id="header">
    <h1>
      Simple News!
    </h1>
    <p v-if="username">Bienvenido, {{ username }}!</p>
    <div class="navbar-container">
      <Navbar />
    </div>
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
import { useAuthStore } from './stores/authStore'
import { computed } from 'vue'
import { jwtDecode } from 'jwt-decode'

const auth = useAuthStore()

const username = computed(() => {
  if (!auth.token) return null
  try {
    const decoded: any = jwtDecode(auth.token)
    return decoded.username || decoded.sub || null
  } catch {
    return null
  }
})

const year = new Date().getFullYear();
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=PT+Serif:wght@400;700&display=swap');

:root {
  --nyt-black: #121212;
  --nyt-gray: #f8f8f8;
  --nyt-border: #e2e2e2;
  --nyt-red: #e63946;
}

body {
  font-family: 'PT Serif', Georgia, 'Times New Roman', Times, serif;
  background: var(--nyt-gray);
  color: var(--nyt-black);
  margin: 0;
  padding: 0;
}

#header {
  background: #fff;
  border-bottom: 1.5px solid var(--nyt-border);
  padding: 2rem 0 1rem 0;
  text-align: center;
  letter-spacing: 1px;
}

#header h1 {
  font-family: 'PT Serif', Georgia, 'Times New Roman', Times, serif;
  font-size: 2.8rem;
  font-weight: 700;
  letter-spacing: 2px;
  margin: 0;
  color: var(--nyt-black);
}

#header p {
  font-size: 1.1rem;
  color: #666;
  margin: 0.5rem 0 0 0;
}

main {
  max-width: 800px;
  margin: 2rem auto 2rem auto;
  background: #fff;
  padding: 2rem 2.5rem;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
  border: 1px solid var(--nyt-border);
  min-height: 60vh;
}

.navbar-container {
  max-width: 800px;
  margin: 0 auto;
}

footer {
  background: #fff;
  border-top: 1.5px solid var(--nyt-border);
  text-align: center;
  padding: 1.2rem 0 1rem 0;
  font-size: 1rem;
  color: #888;
  letter-spacing: 1px;
  margin-top: 2rem;
}

a {
  color: var(--nyt-red);
  text-decoration: none;
  transition: color 0.2s;
}
a:hover {
  text-decoration: underline;
  color: #a4161a;
}

nav {
  margin: 1.5rem 0 0.5rem 0;
  display: flex;
  justify-content: center;
  gap: 2rem;
  border-bottom: 1px solid var(--nyt-border);
  padding-bottom: 0.5rem;
}

nav a {
  font-family: 'PT Serif', serif;
  font-size: 1.1rem;
  color: var(--nyt-black);
  font-weight: 500;
  padding: 0.2rem 0.5rem;
  border-radius: 2px;
}

nav a.router-link-exact-active {
  border-bottom: 2px solid var(--nyt-red);
  color: var(--nyt-red);
}

@media (max-width: 900px) {
  main {
    max-width: 98vw;
    padding: 1rem;
    min-height: 50vh;
  }
  #header h1 {
    font-size: 2rem;
  }
  .navbar-container {
    max-width: 98vw;
    padding: 0 0.5rem;
  }
  nav {
    gap: 1rem;
    flex-wrap: wrap;
    font-size: 1rem;
    padding-bottom: 0.3rem;
  }
  footer {
    font-size: 0.9rem;
    padding: 0.8rem 0 0.8rem 0;
  }
}

@media (max-width: 600px) {
  main {
    padding: 0.5rem;
    font-size: 0.98rem;
  }
  #header {
    padding: 1rem 0 0.5rem 0;
  }
  #header h1 {
    font-size: 1.3rem;
    letter-spacing: 1px;
  }
  .navbar-container {
    padding: 0 0.2rem;
  }
  nav {
    gap: 0.5rem;
    font-size: 0.95rem;
    flex-direction: column;
    align-items: center;
  }
  footer {
    font-size: 0.85rem;
    padding: 0.5rem 0 0.5rem 0;
  }
}
</style>
