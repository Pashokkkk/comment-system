<template>
  <div class="comment" style="margin-bottom: 15px;">
    <p><strong>{{ comment.username }}</strong> ({{ comment.email }})</p>
    <p v-html="comment.text"></p>

    <!-- Preview image with lightbox -->
    <div v-if="isImage(comment.file_upload)">
      <img
        :src="comment.file_upload"
        @click="showLightbox = true"
        class="comment-image-preview"
      />
      <VueEasyLightbox
        :visible="showLightbox"
        :imgs="[comment.file_upload]"
        @hide="showLightbox = false"
      />
    </div>

    <!-- File download link if it's a text file -->
    <div v-else-if="isTextFile(comment.file_upload)">
      <a :href="comment.file_upload" target="_blank">Download attached file</a>
    </div>

    <p style="font-size: 12px; color: gray;">{{ new Date(comment.created_at).toLocaleString() }}</p>

    <!-- Render replies recursively -->
    <div class="replies" style="margin-left: 30px;" v-if="comment.replies && comment.replies.length">
      <comment-item
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import VueEasyLightbox from 'vue-easy-lightbox'

defineProps({
  comment: Object
})

const showLightbox = ref(false)

function isImage(url) {
  return /\.(jpg|jpeg|png|gif)$/i.test(url)
}

function isTextFile(url) {
  return /\.txt$/i.test(url)
}
</script>

<style>
.comment-image-preview {
  max-width: 150px;
  max-height: 100px;
  cursor: pointer;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-top: 8px;
}
</style>
