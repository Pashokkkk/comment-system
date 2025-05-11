<template>
  <div>
    <h2>🗨 All Comments</h2>

    <div v-if="loading" class="loader">Loading comments...</div>

    <div v-else>
      <comment-item
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
      />
    </div>

    <div v-if="successMessage" class="success">{{ successMessage }}</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

    <!-- PAGINATION -->
    <div class="pagination" style="margin-top: 20px;">
      <button :disabled="page === 1" @click="page--">Previous</button>
      <span>Page {{ page }}</span>
      <button :disabled="!hasMore" @click="page++">Next</button>
    </div>
  </div>
</template>

<script>
import CommentItem from './CommentItem.vue';

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
      successMessage: '',
      errorMessage: '',
    };
  },
  watch: {
    page: 'fetchComments'
  },
  mounted() {
    this.fetchComments();
    this.interval = setInterval(this.fetchComments, 5000);
  },
  beforeUnmount() {
    clearInterval(this.interval);
  },
  methods: {
    async fetchComments() {
      this.loading = true;
      const url = `http://localhost:8000/api/comments/?page=${this.page}`;
      try {
        const res = await fetch(url);
        const data = await res.json();
        this.comments = data.results;
        this.hasMore = !!data.next;
      } catch (err) {
        console.error('Failed to load comments', err);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
<style>
.loader {
  text-align: center;
  margin: 20px;
  font-weight: bold;
  color: #555;
}
</style>
