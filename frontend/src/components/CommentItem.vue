<template>
  <div class="comment" style="margin-bottom: 15px;">
    <p><strong>{{ comment.username }}</strong> ({{ comment.email }})</p>
    <p v-html="comment.text"></p>
    <p style="font-size: 12px; color: gray;">{{ new Date(comment.created_at).toLocaleString() }}</p>

    <!-- Відповіді, якщо є -->
    <div class="replies" style="margin-left: 30px;" v-if="comment.replies && comment.replies.length">
      <comment-item
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: "CommentItem",
  props: {
    comment: Object,
  }
};
</script>
