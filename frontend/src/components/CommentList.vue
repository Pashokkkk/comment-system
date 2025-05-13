<template>
  <div>
    <h2>🗨 All Comments</h2>

    <!-- Sort options -->
    <select v-model="ordering" @change="fetchComments">
      <option value="-created_at">Newest</option>
      <option value="created_at">Oldest</option>
      <option value="username">Username A→Z</option>
      <option value="-username">Username Z→A</option>
      <option value="email">Email A→Z</option>
      <option value="-email">Email Z→A</option>
    </select>

    <!-- Loading indicator -->
    <div v-if="loading" class="loader">Loading comments...</div>

    <!-- Render comment items -->
    <div v-else>
      <comment-item
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
      />
    </div>

    <!-- Pagination controls -->
    <div class="pagination" style="margin-top: 20px;">
      <button :disabled="page === 1" @click="page--">Previous</button>
      <span>Page {{ page }}</span>
      <button :disabled="!hasMore" @click="page++">Next</button>
    </div>
  </div>
</template>

<script>
import CommentItem from './CommentItem.vue'

export default {
  components: { CommentItem },
  data() {
    return {
      comments: [],
      page: 1,
      pageSize: 25,
      hasMore: true,
      interval: null,
      loading: false,
      ordering: '-created_at',
    }
  },
  watch: {
    // Fetch comments on page change
    page: 'fetchComments'
  },
  mounted() {
    // Initial fetch
    this.fetchComments()

    // Open WebSocket connection
    const socket = new WebSocket("ws://" + window.location.hostname + ":8000/ws/comments/")

    // Handle incoming comment (only top-level)
    socket.onmessage = (event) => {
      const newComment = JSON.parse(event.data)

      // Add only top-level comments (not replies)
      if (!newComment.parent_comment) {
        this.comments.unshift(newComment)
      }
    }
  },
  beforeUnmount() {
    // Clean up intervals if used
    clearInterval(this.interval)
  },
  methods: {
    // Fetch paginated & sorted comments
    async fetchComments() {
      this.loading = true
      const url = `http://localhost:8000/api/comments/?page=${this.page}&ordering=${this.ordering}`

      try {
        const res = await fetch(url)
        const data = await res.json()
        this.comments = data.results
        this.hasMore = !!data.next
      } catch (err) {
        console.error('Failed to load comments', err)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style>
.loader {
  text-align: center;
  margin: 20px;
  font-weight: bold;
  color: #555;
}
.comment-content strong {
  font-weight: bold;
}
</style>
