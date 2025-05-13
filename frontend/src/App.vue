<script setup>
import { ref, onMounted } from 'vue'
import CommentForm from './components/CommentForm.vue'
import CommentList from './components/CommentList.vue'
import LoginForm from './components/LoginForm.vue'

const isLoggedIn = ref(false)
const justLoggedOut = ref(false)

// Check if stored token is valid
async function checkTokenValidity() {
  const token = localStorage.getItem('access')
  if (!token) {
    isLoggedIn.value = false
    return
  }

  try {
    const res = await fetch('http://localhost:8000/api/comments/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    isLoggedIn.value = res.ok
  } catch (err) {
    isLoggedIn.value = false
  }
}

// Check token on app load
onMounted(() => {
  checkTokenValidity()
})

// Handle login success from child component
function handleLoginSuccess() {
  isLoggedIn.value = true
  justLoggedOut.value = false
}

// Clear tokens and log out
function logout() {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  isLoggedIn.value = false
  justLoggedOut.value = true
}
</script>

<template>
  <div>
    <!-- Authenticated view -->
    <div v-if="isLoggedIn">
      <button @click="logout">Logout</button>
      <CommentForm />
      <hr />
      <CommentList />
    </div>

    <!-- Unauthenticated view -->
    <div v-else>
      <LoginForm @login-success="handleLoginSuccess" />
      <p v-if="justLoggedOut" class="info">
        🔓 You have been logged out. Please log in again.
      </p>
    </div>
  </div>
</template>

<style scoped>
.info {
  background-color: #eaf4ff;
  color: #333;
  padding: 10px;
  border-left: 5px solid #2196F3;
  margin-top: 10px;
}
</style>
