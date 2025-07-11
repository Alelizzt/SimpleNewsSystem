<template>
  <div>
    Registrate para informar al mundo de las noticias que te importan.
    <form id="register-form" @submit.prevent="handleNewRegister">
      <label for="username">Nombre de usuario:</label>
      <input type="text" id="username" v-model="user.username" required />

      <label for="email">Correo electrónico:</label>
      <input type="email" id="email" v-model="user.email" required />

      <label for="password">Contraseña:</label>
      <input type="password" id="password" v-model="user.password" required />

      <label for="repeatPassword">Repite la contraseña:</label>
      <input type="password" id="repeatPassword" v-model="repeatPassword" required />

      <button type="submit">Registrarse</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { register } from '../services/authService'

const user = ref({
  username: '',
  email: '',
  password: ''
})
const repeatPassword = ref('')

async function handleNewRegister() {
  if (user.value.password !== repeatPassword.value) {
    alert('Las contraseñas no coinciden')
    return
  }
  try {
    await register( user.value.email, user.value.password, user.value.username)
    alert('Usuario registrado correctamente')
    // Opcional: limpiar el formulario
    user.value = { username: '', email: '', password: '' }
    repeatPassword.value = ''
  } catch (error) {
    console.error('Error al registrar usuario:', error)
    alert('Error al registrar usuario')
  }
}
</script>

<style scoped>
#register-form {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem 2.5rem;
  background: #faf9f7;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(30, 30, 30, 0.04);
  font-family: 'PT Serif', Georgia, 'Times New Roman', Times, serif;
}

#register-form label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 700;
  color: #222;
  font-size: 1.05rem;
  letter-spacing: 0.5px;
}

#register-form input[type="text"],
#register-form input[type="email"],
#register-form input[type="password"] {
  width: 100%;
  padding: 0.6rem 0.8rem;
  margin-bottom: 1.2rem;
  border: 1px solid #d3d3d3;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
  background: #fff;
  transition: border-color 0.2s;
}

#register-form input:focus {
  border-color: #121212;
  outline: none;
}

#register-form button[type="submit"] {
  width: 100%;
  padding: 0.7rem 0;
  background: #121212;
  color: #fff;
  font-family: inherit;
  font-size: 1.1rem;
  font-weight: 700;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  letter-spacing: 1px;
  transition: background 0.2s;
}

#register-form button[type="submit"]:hover {
  background: #333;
}

div {
  font-family: 'PT Serif', Georgia, 'Times New Roman', Times, serif;
  color: #222;
  text-align: center;
  margin-top: 2rem;
  font-size: 1.15rem;
}
</style>