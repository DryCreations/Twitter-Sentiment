<template>
  <div class="Tweet">
    <TopBar title="Tweet"/>
  </div>
</template>

<script>
// @ is an alias to /src
import TopBar from '@/components/TopBar.vue'
import axios from 'axios'

export default {
  name: 'Tweet',
  components: {
    TopBar
  },
  created () {
    axios.post('/api/sentiment', {
      keywords: ['test']
    }).then(function (response) {
      console.log(response)
    })
  }
}
</script>
