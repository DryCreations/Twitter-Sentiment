<template>
  <div id="app">
    <router-view/>
    <div id="nav">
      <router-link to="/">Keyword</router-link> |
      <router-link to="/Tweet">Tweet</router-link> |
      <router-link to="/Chart">Chart</router-link>
    </div>

    <p>{{ isLoggedIn ? 'yes' : 'no' }}</p>
  </div>
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
  overflow: hidden;
  background-color: #d1fff2;
  position: fixed; /* Set the navbar to fixed position */
  bottom: 0px; /* Position the navbar at the top of the page */
  width: 100%; /* Full width */

  a {
    font-weight: bold;
    color: #346eeb;

    &.router-link-exact-active {
      color: #34aeeb;
    }
  }
}
</style>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState(['isLoggedIn'])
  },
  created () {
    this.$store.dispatch('check_login')
  }
}
</script>
