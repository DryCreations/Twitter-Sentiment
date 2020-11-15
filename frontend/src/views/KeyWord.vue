<template>
  <div class="KeyWord">
    <TopBar title="KeyWord"/>
    <input type="text" id="keywordInput" value="" v-model="keywordInput" />
    <input type="button" id="addKeyword" value="addKeyword" v-on:click="addKeyword()" />
    <br>
    <p v-for="term in searchTerms" v-bind:key="term">
      {{ term }}
    </p>
    <input type="button" id="search" value="search" v-on:click="search()" />
  </div>
</template>

<script>
// @ is an alias to /src
import TopBar from '@/components/TopBar.vue'
import { mapState } from 'vuex'

export default {
  name: 'KeyWord',
  components: {
    TopBar
  },
  data: () => ({
    keywordInput: ''
  }),
  computed: {
    ...mapState(['searchTerms'])
  },
  methods: {
    addKeyword: function () {
      this.$store.dispatch('add_keyword', this.keywordInput)
      this.keywordInput = []
    },
    search: function () {
      this.$store.dispatch('get_tweets', this.searchTerms)
    }
  }
}
</script>
