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
      <input v-model="captchaText" required />
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

<script>
export default {
  data() {
    return {
      form: {
        username: '',
        email: '',
        homepage_url: '',
        text: '',
        captcha_text: '',
        captcha_key: '',
        file: null
      },
      captchaImageUrl: '',
      previewVisible: false,
      successMessage: '',
      errorMessage: ''
    };
  }
  mounted() {
    this.refreshCaptcha();
  },
  methods: {
    async refreshCaptcha() {
      try {
        const res = await fetch("http://localhost:8000/api/captcha/refresh/");
        const data = await res.json();
        this.form.captcha_key = data.key;
        this.captchaImageUrl = data.image_url;
        this.form.captcha_text = '';
      } catch (error) {
        console.error("❌ Failed to refresh CAPTCHA", error);
      }
    },
    handleFile(event) {
      this.form.file = event.target.files[0];
    },
    insertTag(tag) {
      this.form.text += `<${tag}></${tag}>`;
    },
    insertLink() {
      this.form.text += `<a href='https://'>link</a>`;
    },
    async handleSubmit() {
      if (!this.form.username || !this.form.email || !this.form.text || !this.form.captcha_text) {
        this.errorMessage = "⚠️ Please fill in all required fields!";
        return;
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.form.email)) {
        this.errorMessage = "⚠️ Please enter a valid email address!";
        return;
      }

      const formData = new FormData();
      for (const key in this.form) {
        if (this.form[key]) {
          formData.append(key, this.form[key]);
        }
      }

      try {
        const response = await fetch("http://localhost:8000/api/comments/", {
          method: "POST",
          body: formData
        });

        if (!response.ok) {
          const err = await response.json();
          throw new Error(err?.captcha_text?.[0] || "Failed to submit");
        }

        this.successMessage = "✅ Comment submitted!";
        this.errorMessage = "";

        this.form = {
          username: '',
          email: '',
          homepage_url: '',
          text: '',
          captcha_text: '',
          captcha_key: '',
          file: null
        };

        this.refreshCaptcha();
      } catch (error) {
        this.successMessage = "";
        this.errorMessage = "❌ Submission failed: " + error.message;
      }
    }
  }
};
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
