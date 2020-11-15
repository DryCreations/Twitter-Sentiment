import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isLoggedIn: false,
    data: {},
    searchTerms: [],
    searchCompleted: false,
    pendingSearch: false
  },
  mutations: {
    set_login: (state, event) => {
      state.isLoggedIn = event.data.loggedIn
    },
    set_data: (state, event) => {
      state.data = event.data
    },
    add_search: (state, event) => {
      state.searchTerms.push(event.data)
    },
    search_status: (state, event) => {
      state.searchCompleted = event.data
    },
    pending_query_status: (state, event) => {
      state.pendingSearch = event.data
    }
  },
  actions: {
    check_login: (state) => {
      axios.get('/api/check_auth').then((response) => {
        console.log(response)
        state.commit('set_login', response)
      })
    },
    get_tweets: (state, keywords) => {
      state.commit('pending_query_status', { data: true })
      axios.post('/api/sentiment', {
        keywords: keywords
      }).then((response) => {
        console.log(response)
        state.commit('set_data', response)
        state.commit('search_status', { data: true })
        state.commit('pending_query_status', { data: false })
      })
    },
    add_keyword: (state, keyword) => {
      state.commit('add_search', { data: keyword })
    }
  },
  modules: {
  }
})
