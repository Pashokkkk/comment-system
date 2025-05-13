<template>
  <div>
    <!-- Placeholder for optional pre-login form -->
    <form v-if="!isLoggedIn">
    </form>
  </div>

  <div class="login-form">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
    <p v-if="error" style="color: red;">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// Emit login success event to parent
const emit = defineEmits(['login-success'])

const username = ref('')
const password = ref('')
const error = ref('')
const isLoggedIn = ref(false)

// Check if token already exists
onMounted(() => {
  const token = localStorage.getItem('access')
  isLoggedIn.value = !!token
})

// Send login request and handle response
const login = async () => {
  error.value = ''
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/token/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username: username.value, password: password.value })
    })

    if (!response.ok) throw new Error('Login failed')

    const data = await response.json()

    // Store tokens in localStorage
    localStorage.setItem('access', data.access)
    localStorage.setItem('refresh', data.refresh)

    alert('Login successful! ✅')

    // Notify parent about login
    emit('login-success')

  } catch (err) {
    // Show error message
    error.value = err.message
  }
}
</script>

<style scoped>
.login-form {
  max-width: 300px;
  margin: 20px auto;
}
input {
  display: block;
  margin: 10px 0;
  width: 100%;
  padding: 8px;
}
button {
  padding: 8px 16px;
}
</style>
