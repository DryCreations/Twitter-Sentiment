<template>
  <div class="Tweet">
    <TopBar title="Tweet"/>
    <div v-for="tweet in data.tweets" class="tweetCard" v-bind:key="tweet.id">
      <p> {{ tweet.full_text }} </p>
      <p> sentiment: {{ tweet.sentiment }} </p>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import TopBar from '@/components/TopBar.vue'
import { mapState } from 'vuex'

export default {
  name: 'Tweet',
  components: {
    TopBar
  },
  computed: {
    ...mapState(['data'])
  }
}
</script>

<style>
.tweetCard {
  padding: 10px;
}
</style>
