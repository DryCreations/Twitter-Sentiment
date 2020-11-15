<script>
import { Pie } from 'vue-chartjs'
export default {
  props: ['pieChartData', 'pieOptions'],
  extends: Pie,
  mounted () {
    this.renderChart(this.pieChartData, this.pieOptions)
  }
}

</script>
