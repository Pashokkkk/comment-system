<template>
  <form @submit.prevent="handleSubmit">
    <div>
      <label>Username:</label>
      <input v-model="form.username" required />
    </div>
    <div>
      <label>Email:</label>
      <input type="email" v-model="form.email" required />
    </div>
    <div>
      <label>Homepage URL:</label>
      <input type="url" v-model="form.homepage_url" />
    </div>
    <div>
      <label>Comment Text:</label>
      <div class="tag-buttons" style="margin-bottom: 10px;">
        <button type="button" @click="insertTag('i')">[i]</button>
        <button type="button" @click="insertTag('strong')">[strong]</button>
        <button type="button" @click="insertTag('code')">[code]</button>
        <button type="button" @click="insertLink">[a]</button>
      </div>
      <textarea v-model="form.text" required></textarea>
    </div>

    <!-- CAPTCHA -->
    <div>
      <label>Enter CAPTCHA:</label>
      <img :src="captchaImageUrl" alt="captcha" />
      <button type="button" @click="refreshCaptcha">🔁 Refresh</button>
      <input v-model="form.captcha_text" required />
    </div>

    <div>
      <label>Upload File (optional):</label>
      <input type="file" @change="handleFile" accept=".jpg,.jpeg,.png,.txt,.md" />
    </div>

    <button type="button" @click="previewVisible = !previewVisible">
      {{ previewVisible ? 'Hide Preview' : 'Show Preview' }}
    </button>

    <div v-if="previewVisible" style="border: 1px solid #ccc; padding: 10px; margin-top: 10px;">
      <h4>Preview:</h4>
      <p><strong>{{ form.username }}</strong> ({{ form.email }})</p>
      <p v-html="form.text"></p>
    </div>

    <!-- NOTIFICATIONS -->
    <div v-if="successMessage" class="success">{{ successMessage }}</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

    <button type="submit">Submit</button>
  </form>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

const form = reactive({
  username: '',
  email: '',
  homepage_url: '',
  text: '',
  captcha_text: '',
  captcha_key: '',
  file: null
})

const captchaImageUrl = ref('')
const previewVisible = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

onMounted(() => {
  console.log("🚀 CommentForm mounted")
  refreshCaptcha()
})

async function refreshCaptcha() {
  try {
    const res = await fetch("http://localhost:8000/api/captcha/refresh/")
    const data = await res.json()
    form.captcha_key = data.key
    captchaImageUrl.value = "http://localhost:8000" + data.image_url
    form.captcha_text = ''
  } catch (error) {
    console.error("❌ Failed to refresh CAPTCHA", error)
  }
}

function handleFile(event) {
  console.log("✅ handleFile triggered")
  form.file = event.target.files[0]
  console.log("📦 Selected file:", form.file)
}

function insertTag(tag) {
  form.text += `<${tag}></${tag}>`
}

function insertLink() {
  form.text += `<a href='https://'>link</a>`
}

async function handleSubmit() {
  if (!form.username || !form.email || !form.text || !form.captcha_text) {
    errorMessage.value = "⚠️ Please fill in all required fields!"
    return
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(form.email)) {
    errorMessage.value = "⚠️ Please enter a valid email address!"
    return
  }

  const formData = new FormData()
  Object.entries(form).forEach(([key, value]) => {
    if (value) {
      if (key === 'file') {
        formData.append('file_upload', value)
      } else {
        formData.append(key, value)
      }
    }
  })

  try {
    const response = await fetch("http://localhost:8000/api/comments/", {
      method: "POST",
      body: formData
    })

    if (!response.ok) {
      const err = await response.json()
      throw new Error(err?.captcha_text?.[0] || err?.text?.[0] || "Failed to submit")
    }

    successMessage.value = "✅ Comment submitted!"
    errorMessage.value = ""

    // Reset form
    form.username = ''
    form.email = ''
    form.homepage_url = ''
    form.text = ''
    form.captcha_text = ''
    form.captcha_key = ''
    form.file = null

    refreshCaptcha()
  } catch (error) {
    successMessage.value = ''
    errorMessage.value = "❌ Submission failed: " + error.message
  }
}
</script>

<style>
.success {
  background-color: #d4edda;
  color: #155724;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #c3e6cb;
  border-radius: 5px;
}
.error {
  background-color: #f8d7da;
  color: #721c24;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #f5c6cb;
  border-radius: 5px;
}
</style>
