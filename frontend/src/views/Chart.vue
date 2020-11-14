<template>
  <div class="Chart">
    <TopBar title="Chart"/>
    <PieChart :chartData="chartData" :options="options"/>
  </div>
</template>

<script>
// @ is an alias to /src
import TopBar from '@/components/TopBar.vue'
import PieChart from '@/components/PieChart.vue'

export default {
  data: () => ({
    chartData: {
      datasets: [{
        data: [10, 20, 30],
        backgroundColor: ['#f87979', '#45f542', '#707070']
      }],
      // These labels appear in the legend and in the tooltips when hovering different arcs
      labels: [
        'Negative',
        'Postive',
        'Unsure'
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  }),
  name: 'Chart',
  components: {
    TopBar,
    PieChart
  }
}
</script>
