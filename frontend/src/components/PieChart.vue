<script>
import { Pie } from 'vue-chartjs'
export default {
  props: ['chartData', 'options'],
  extends: Pie,
  mounted () {
    this.renderChart(this.chartData, this.options)
  }
}

</script>
