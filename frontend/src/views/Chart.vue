<template>
  <div class="Chart">
    <TopBar title="Chart"/>
    <PieChart :pieChartData="sentimentPieChartData" :pieOptions="sentimentPieChartOptions"/>
    <BarChart :barChartData="numAccountTweetsBarChartData" :numAccountTweetsBarChartOptions="barOptions"/>
    <LineChart :lineChartData="lineChartData" :lineOptions="lineOptions"/>
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
  data: () => ({
    totalTweetsLineChartData: {
      datasets: [{
        label: 'Total Tweets',
        data: [20, 70, 50, 30, 123, 47, 56],
        backgroundColor: '#f87979'
      }],
      // These labels appear in the legend and in the tooltips when hovering different arcs
      labels: [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday'
      ]
    },
    totalTweetsLineOptions: {
      scales: {
        yAxes: [{
          stacked: false
        }]
      }
    }
  }),
  computed: mapState({
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
      const nameList = {}
      for (let i = 0; i < state.data.tweets.length; i++) {
        const currentName = state.data.tweets[i].user.screen_name
        if (currentName in nameList) {
          nameList[currentName]++
        } else {
          nameList[currentName] = 1
        }
      }
      const tempValue = Object.values(nameList)
      const tempKeys = Object.keys(nameList)
      console.log(tempValue)
      console.log(tempKeys)
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
