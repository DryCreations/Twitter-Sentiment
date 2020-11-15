<script>
import { Line } from 'vue-chartjs'
export default {
  props: ['lineChartData', 'lineOptions'],
  extends: Line,
  mounted () {
    this.renderChart(this.lineChartData, this.lineOptions)
  }
}

</script>
