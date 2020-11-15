<template>
  <div class="Chart">
    <TopBar title="Chart"/>
    <PieChart v-if="displayCharts" :pieChartData="sentimentPieChartData" :pieOptions="sentimentPieChartOptions"/>
    <!-- <BarChart :barChartData="barChartData" :barOptions="barOptions"/>
    <LineChart :lineChartData="lineChartData" :lineOptions="lineOptions"/> -->
  </div>
</template>

<script>
// @ is an alias to /src
import TopBar from '@/components/TopBar.vue'
import PieChart from '@/components/PieChart.vue'
// import BarChart from '@/components/BarChart.vue'
// import LineChart from '@/components/LineChart.vue'

import { mapState } from 'vuex'

export default {
  // data: () => ({
  //   lineChartData: {
  //     datasets: [{
  //       label: 'Line 1',
  //       data: [20, 70, 50, 30, 123, 47, 56],
  //       backgroundColor: '#f87979'
  //     }, {
  //       label: 'Line 2',
  //       data: [70, 50, 30, 123, 47, 56, 20],
  //       backgroundColor: '#45f542'
  //     }],
  //     // These labels appear in the legend and in the tooltips when hovering different arcs
  //     labels: [
  //       'Sunday',
  //       'Monday',
  //       'Tuesday',
  //       'Wednesday',
  //       'Thursday',
  //       'Friday',
  //       'Saturday'
  //     ]
  //   },
  //   lineOptions: {
  //     scales: {
  //       yAxes: [{
  //         stacked: false
  //       }]
  //     }
  //   }
  // }),
  computed: mapState({
    displayCharts: function (state) {
      console.log(state.searchCompleted)
      console.log(state.pendingSearch)
      return state.searchCompleted && !state.pendingSearch
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
    }
    // barChartData: function (state) {
    //   return {
    //     datasets: [{
    //       label: 'Neg',
    //       barPercentage: 0.5,
    //       barThickness: 10,
    //       maxBarThickness: 8,
    //       minBarLength: 2,
    //       data: [20, 70, 50, 30, 123, 47, 56],
    //       backgroundColor: '#f87979'
    //     }, {
    //       label: 'Pos',
    //       barPercentage: 0.5,
    //       barThickness: 10,
    //       maxBarThickness: 8,
    //       minBarLength: 2,
    //       data: [70, 50, 30, 123, 47, 56, 20],
    //       backgroundColor: '#45f542'
    //     }],
    //     // These labels appear in the legend and in the tooltips when hovering different arcs
    //     labels: [
    //       'Sunday',
    //       'Monday',
    //       'Tuesday',
    //       'Wednesday',
    //       'Thursday',
    //       'Friday',
    //       'Saturday'
    //     ]
    //   }
    // },
    // barOptions: function (state) {
    //   return {
    //     scales: {
    //       xAxes: [{
    //         gridLines: {
    //           offsetGridLines: true
    //         }
    //       }]
    //     }
    //   }
    // }
  }),
  name: 'Chart',
  components: {
    TopBar,
    PieChart
    // BarChart,
    // LineChart
  }
}
</script>
