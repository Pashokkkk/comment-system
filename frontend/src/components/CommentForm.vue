<template>
  <form @submit.prevent="handleSubmit" class="comment-form">
    <h2>💬 Leave a Comment</h2>

    <div class="form-group">
      <label>Username:</label>
      <input v-model="form.username" type="text" required />
    </div>

    <div class="form-group">
      <label>Email:</label>
      <input v-model="form.email" type="email" required />
    </div>

    <div class="form-group">
      <label>Homepage URL:</label>
      <input v-model="form.homepage_url" type="url" />
    </div>

    <div class="form-group">
      <label>Comment Text:</label>
      <div class="tag-buttons">
        <button type="button" @click="insertTag('i')">[i]</button>
        <button type="button" @click="insertTag('strong')">[strong]</button>
        <button type="button" @click="insertTag('code')">[code]</button>
        <button type="button" @click="insertLink">[a]</button>
      </div>
      <textarea v-model="form.text" required rows="4"></textarea>
    </div>

    <div class="form-group captcha-group">
      <label>Enter CAPTCHA:</label>
      <img :src="captchaImageUrl" alt="captcha" class="captcha-img" />
      <button type="button" @click="refreshCaptcha" class="refresh-btn">🔄</button>
      <input v-model="form.captcha_text" type="text" required />
    </div>

    <div class="form-group">
      <label>Upload File (optional):</label>
      <input type="file" @change="handleFile" />
    </div>

    <div class="form-actions">
      <button type="button" @click="previewVisible = !previewVisible">
        {{ previewVisible ? 'Hide Preview' : 'Show Preview' }}
      </button>
      <button type="submit" class="submit-btn">Submit</button>
    </div>

    <div v-if="previewVisible" class="preview">
      <h4>📄 Preview:</h4>
      <p><strong>{{ form.username }}</strong> ({{ form.email }})</p>
      <p v-html="form.text"></p>
    </div>

    <div v-if="successMessage" class="alert success">{{ successMessage }}</div>
    <div v-if="errorMessage" class="alert error">{{ errorMessage }}</div>
  </form>
</template>

<script setup>
// Import Vue features
import { ref, reactive, onMounted } from 'vue'

// Form state with all necessary fields
const form = reactive({
  username: '',
  email: '',
  homepage_url: '',
  text: '',
  captcha_text: '',
  captcha_key: '',
  file: null
})

// Props to handle optional parent comment ID
const props = defineProps({
  parentId: Number
})

// State for captcha, preview, and messages
const captchaImageUrl = ref('')
const previewVisible = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

// Fetch initial CAPTCHA when component is mounted
onMounted(() => {
  console.log("🚀 CommentForm mounted")
  refreshCaptcha()
})

// Fetch a new CAPTCHA image and key
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

// Handle file input and store selected file in form
function handleFile(event) {
  form.file = event.target.files[0]
  console.log("📦 Selected file:", form.file)
}

// Insert basic HTML formatting tags into the comment text
function insertTag(tag) {
  form.text += `<${tag}></${tag}>`
}

function insertLink() {
  form.text += `<a href="https://">link</a>`
}

// Validate and submit the comment form
async function handleSubmit() {
  errorMessage.value = ""
  successMessage.value = ""

  // Basic validation
  if (!form.username || !form.email || !form.text || !form.captcha_text) {
    errorMessage.value = "⚠️ Please fill in all required fields!"
    return
  }

  // Validate email format
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(form.email)) {
    errorMessage.value = "⚠️ Please enter a valid email address!"
    return
  }

  // Check for token
  const token = localStorage.getItem("access")
  if (!token) {
    errorMessage.value = "🔒 You are not logged in. Please log in."
    return
  }

  // Prepare form data for submission
  const formData = new FormData()
  formData.append("username", form.username)
  formData.append("email", form.email)
  formData.append("homepage_url", form.homepage_url || "")
  formData.append("text", form.text)
  formData.append("captcha_key", form.captcha_key)
  formData.append("captcha_text", form.captcha_text)

  if (props.parentId) {
    formData.append("parent_comment", props.parentId)
  }

  if (form.file) {
    formData.append("file_upload", form.file)
  }

  // Submit the form
  try {
    const response = await fetch("http://localhost:8000/api/comments/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    })

    const contentType = response.headers.get("content-type")

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error("🔒 Unauthorized. Please log in again.")
      } else if (response.status === 500) {
        throw new Error("💥 Server error. Try again later.")
      }

      // Show specific error if available
      if (contentType && contentType.includes("application/json")) {
        const err = await response.json()
        throw new Error(
          err?.captcha_text?.[0] || err?.text?.[0] || err?.detail || "❌ Failed to submit"
        )
      } else {
        const errText = await response.text()
        throw new Error(`❌ Unexpected server response: ${errText}`)
      }
    }

    // Show success and reset form
    successMessage.value = "✅ Comment submitted!"
    form.username = ""
    form.email = ""
    form.homepage_url = ""
    form.text = ""
    form.captcha_text = ""
    form.captcha_key = ""
    form.file = null
    refreshCaptcha()
  } catch (error) {
    errorMessage.value = error.message
    console.error("❌ Submit error:", error)
  }
}
</script>

<style scoped>
/* Basic styling for the comment form UI */
.comment-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background: #fdfdfd;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.05);
}

h2 {
  margin-bottom: 15px;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

input[type="text"],
input[type="email"],
input[type="url"],
input[type="file"],
textarea {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

textarea {
  resize: vertical;
}

.tag-buttons button {
  margin-right: 5px;
  padding: 5px 8px;
  border: none;
  background: #eee;
  border-radius: 4px;
  cursor: pointer;
}

.tag-buttons button:hover {
  background: #ddd;
}

.captcha-group {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.captcha-img {
  height: 40px;
  border: 1px solid #ccc;
}

.refresh-btn {
  background: #f0f0f0;
  border: none;
  padding: 6px;
  border-radius: 4px;
  cursor: pointer;
}

.refresh-btn:hover {
  background: #e0e0e0;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}

.submit-btn {
  background-color: #4CAF50;
  color: white;
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.submit-btn:hover {
  background-color: #45a049;
}

.preview {
  background: #f8f8f8;
  padding: 10px;
  margin-top: 10px;
  border-left: 3px solid #2196F3;
}

.alert {
  margin-top: 10px;
  padding: 10px;
  border-radius: 6px;
}

.success {
  background-color: #d4edda;
  color: #155724;
}

.error {
  background-color: #f8d7da;
  color: #721c24;
}
</style>
