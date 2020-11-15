import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isLoggedIn: false,
    data: {},
    searchTerms: []
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
      axios.post('/api/sentiment', {
        keywords: keywords
      }).then((response) => {
        console.log(response)
        state.commit('set_data', response)
      })
    },
    add_keyword: (state, keyword) => {
      state.commit('add_search', { data: keyword })
    }
  },
  modules: {
  }
})
