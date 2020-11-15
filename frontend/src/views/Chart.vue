<template>
  <div class="Chart">
    <TopBar title="Chart"/>
    <PieChart v-if="displayCharts" :pieChartData="sentimentPieChartData" :pieOptions="sentimentPieChartOptions"/>
    <BarChart v-if="displayCharts" :barChartData="numAccountTweetsBarChartData" :barOptions="numAccountTweetsBarChartOptions"/>
    <LineChart v-if="displayCharts" :lineChartData="totalTweetsLineChartData" :lineOptions="totalTweetsLineOptions"/>
  </div>
</template>

<script>
// @ is an alias to /src
import TopBar from '@/components/TopBar.vue'
import PieChart from '@/components/PieChart.vue'
import BarChart from '@/components/BarChart.vue'
import LineChart from '@/components/LineChart.vue'

import { mapState } from 'vuex'

export default {
  computed: mapState({
    displayCharts: function (state) {
      console.log(state.searchCompleted)
      console.log(state.pendingSearch)
      return state.searchCompleted && !state.pendingSearch
    },
    totalTweetsLineChartData: function (state) {
      const nameList = { Sun: 0, Mon: 0, Tue: 0, Wed: 0, Thu: 0, Fri: 0, Sat: 0 }
      for (let i = 0; i < state.data.tweets.length; i++) {
        if (state.data.tweets[i].created_at.split(' ')[0] in nameList) {
          nameList[state.data.tweets[i].created_at.split(' ')[0]]++
        }
      }
      const tempValue = Object.values(nameList)
      const tempKeys = Object.keys(nameList)
      console.log(tempValue)
      console.log(tempKeys)
      return {
        datasets: [{
          label: 'Total Tweets',
          data: tempValue,
          backgroundColor: '#f87979'
        }],
        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: tempKeys
      }
    },
    totalTweetsLineOptions: function (state) {
      return {
        scales: {
          yAxes: [{
            stacked: false
          }]
        }
      }
    },
    sentimentPieChartData: function (state) {
      let positive = 0
      let negative = 0
      for (let i = 0; i < state.data.tweets.length; i++) {
        const sentiment = state.data.tweets[i].sentiment
        if (sentiment === 'positive') {
          positive++
        } else {
          negative++
        }
      }
      return {
        datasets: [{
          data: [positive, negative],
          backgroundColor: ['#f87979', '#45f542']
        }],
        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: [
          'Negative',
          'Postive'
        ]
      }
    },
    sentimentPieChartOptions: function (state) {
      return {
        responsive: true,
        maintainAspectRatio: false
      }
    },
    numAccountTweetsBarChartData: function (state) {
      let nameList = {}
      for (let i = 0; i < state.data.tweets.length; i++) {
        const currentName = state.data.tweets[i].user.screen_name
        if (currentName in nameList) {
          nameList[currentName]++
        } else {
          nameList[currentName] = 1
        }
      }

      nameList = Object.entries(nameList)

      nameList.sort((i, o) => {
        return o[1] - i[1]
      })

      nameList = Object.fromEntries(nameList.slice(0, 10))

      const tempValue = Object.values(nameList)
      const tempKeys = Object.keys(nameList)

      return {
        datasets: [{
          label: 'Number of Times tweeted with keyword/s',
          barPercentage: 0.5,
          barThickness: 10,
          maxBarThickness: 8,
          minBarLength: 2,
          data: tempValue,
          backgroundColor: '#2d63e0'
        }],
        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: tempKeys
      }
    },
    numAccountTweetsBarChartOptions: function (state) {
      return {
        scales: {
          xAxes: [{
            gridLines: {
              offsetGridLines: true
            }
          }],
          yAxes: [{
            ticks: {
              min: 0,
              stepSize: 1
            }
          }]
        }
      }
    }
  }),
  name: 'Chart',
  components: {
    TopBar,
    PieChart,
    BarChart,
    LineChart
  }
}
</script>
<style>
.Chart{margin-bottom: 100px;}
</style>
