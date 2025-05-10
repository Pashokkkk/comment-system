<template>
  <div>
    <h2>🗨 All Comments</h2>

    <comment-item
      v-for="comment in comments"
      :key="comment.id"
      :comment="comment"
    />

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
    };
  },
  watch: {
    page: 'fetchComments'
  },
  mounted() {
    this.fetchComments();
  },
  methods: {
    async fetchComments() {
      const url = `http://localhost:8000/api/comments/?page=${this.page}`;
      try {
        const res = await fetch(url);
        const data = await res.json();
        this.comments = data.results;
        this.hasMore = !!data.next;
      } catch (err) {
        console.error('Failed to load comments', err);
      }
    }
  }
};
</script>
