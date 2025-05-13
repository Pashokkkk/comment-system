<template>
  <div class="comment">
    <div class="comment-header">
      <div class="comment-avatar"></div>
      <div class="comment-meta">
        <strong>{{ comment.username }}</strong>
        <div class="comment-email">{{ comment.email }}</div>
        <div class="comment-date">{{ new Date(comment.created_at).toLocaleString() }}</div>
      </div>
    </div>

    <!-- Show homepage if available -->
    <p v-if="comment.homepage_url">
      🌐 <a :href="comment.homepage_url" target="_blank" rel="noopener noreferrer">
        {{ comment.homepage_url }}
      </a>
    </p>

    <!-- Display comment content -->
    <div class="comment-content" v-html="comment.text"></div>

    <!-- Show image preview with lightbox -->
    <div v-if="isImage(comment.file_upload)" class="comment-media">
      <a
        :href="resolveUrl(comment.file_upload)"
        data-lightbox="image-set"
        :data-title="comment.username"
      >
        <img
          :src="resolveUrl(comment.file_upload)"
          class="comment-image-preview"
        />
      </a>
    </div>

    <!-- Show download link for text file -->
    <div v-else-if="isTextFile(comment.file_upload)">
      <a :href="resolveUrl(comment.file_upload)" target="_blank">📎 Download attached file</a>
    </div>

    <!-- Display replies recursively -->
    <div class="replies" v-if="comment.replies && comment.replies.length">
      <CommentItem
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
      />
    </div>
  </div>

  <!-- Toggle reply form -->
  <button @click="toggleReply" style="margin-bottom: 20px;">↩️ Reply</button>

  <div v-if="showReplyForm" class="reply-form" style="margin-bottom: 0px;">
    <CommentForm :parentId="comment.id" @submitted="onReplySubmitted" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CommentItem from './CommentItem.vue'
import CommentForm from './CommentForm.vue'

const props = defineProps({
  comment: Object
})

const backendBase = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Resolve full file URL
function resolveUrl(path) {
  if (!path) return ''
  return path.startsWith('http') ? path : backendBase + path
}

// Check if file is an image
function isImage(url) {
  return /\.(jpg|jpeg|png|gif)$/i.test(url || '')
}

// Check if file is a text file
function isTextFile(url) {
  return /\.(txt|md)$/i.test(url || '')
}

const showReplyForm = ref(false)

// Toggle reply form visibility
function toggleReply() {
  showReplyForm.value = !showReplyForm.value
}

// Close reply form after submission
function onReplySubmitted() {
  showReplyForm.value = false
}
</script>

<style scoped>
.comment {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 15px;
  margin-bottom: 5px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
  max-width: 700px;
}

.comment-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.comment-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background-color: #ddd;
  margin-right: 12px;
}

.comment-meta {
  font-size: 14px;
  color: #333;
}

.comment-meta strong {
  display: block;
  font-weight: 600;
  margin-bottom: 2px;
}

.comment-email {
  font-size: 13px;
  color: #777;
}

.comment-date {
  font-size: 12px;
  color: #aaa;
  margin-top: 2px;
}

.comment-content {
  font-size: 15px;
  line-height: 1.5;
  margin-top: 10px;
  margin-bottom: 10px;
}

.comment-image-preview {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
  margin-top: 8px;
  transition: transform 0.3s ease;
  cursor: pointer;
  border: 2px solid transparent;
}

.comment-image-preview:hover {
  transform: scale(1.02);
  border-color: orange;
  box-shadow: 0 0 8px rgba(255, 165, 0, 0.5);
}

.replies {
  margin-top: 20px;
  margin-left: 40px;
  border-left: 2px solid #eee;
  padding-left: 15px;
}

.comment-url {
  font-size: 13px;
  color: #1a0dab;
  margin-top: 4px;
  display: block;
}
</style>
