<script>
import { Bar } from 'vue-chartjs'
export default {
  props: ['barChartData', 'barOptions'],
  extends: Bar,
  mounted () {
    this.renderChart(this.barChartData, this.barOptions)
  }
}

</script>
