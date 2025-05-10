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
    <div>
      <label>Captcha:</label>
      <div>
        <label>Enter CAPTCHA:</label>
        <div style="font-weight: bold; font-size: 20px; letter-spacing: 3px;">{{ generatedCaptcha }}</div>
      </div>
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
        file: null
      },
      generatedCaptcha: '',
      previewVisible: false
    };
  },
  mounted() {
    this.generateCaptcha(); 
  },
  methods: {
    generateCaptcha() {
        const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
        this.generatedCaptcha = Array.from({ length: 5 }, () => chars[Math.floor(Math.random() * chars.length)]).join('');
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
        alert("⚠️ Please fill in all required fields!");
        return;
    }

    if (this.form.captcha_text !== this.generatedCaptcha) {
        alert("⚠️ Incorrect CAPTCHA. Try again.");
        this.generateCaptcha();
        return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(this.form.email)) {
        alert("⚠️ Please enter a valid email address!");
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

        if (!response.ok) throw new Error("Failed to submit");

        alert("✅ Comment submitted!");
        this.form = {
        username: '',
        email: '',
        homepage_url: '',
        text: '',
        captcha_text: '',
        file: null
        };
    } catch (error) {
        alert("❌ Submission failed: " + error.message);
    }
    }

  }
};
</script>
