<template>
  <!-- 为 ECharts 准备一个具备大小（宽高）的 DOM -->
  <div id="chartLine" class="line-wrap"></div>
</template>

<script>
import * as echarts from 'echarts';

require('echarts/theme/shine');//引入主题

export default {
  props: {
    modules: {      //父组件传过来的值
      type: Array
    }
  },
  data() {
    return {
      chartLine: null,
      xAxis: [],
      yAxis: []
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.drawLineChart();
    })
  },

  watch:{
    modules:function(newVal,oldVal){
      if (newVal !== oldVal) {
        this.modules = newVal
        this.drawLineChart()
      }
    }
  },
  methods: {
    drawLineChart() {
      this.chartLine = echarts.init(this.$el, 'shine');
      this.modules.forEach(module => {
          this.xAxis.unshift(module.publish[0].version)
          this.yAxis.unshift(module.module_size)
        })

      let option = {
        tooltip: {
          trigger: 'axis',
          show: false
        },
        legend: {
          data: ['模块大小(byte)']
        },
        calculable: true,
        xAxis: [
          {
            type: 'category',
            boundaryGap: false,
            axisTick: {
              show: true
            },
            data: this.xAxis
          }
        ],
        yAxis: [
          {
            type: 'value',
            axisTick: {
              show: true
            },
          }
        ],
        series: [
          {
            name: '模块大小(byte)',
            type: 'line',
            stack: '总量',
            data: this.yAxis
          }
        ]
      };
      this.chartLine.setOption(option, true);
    },
  }
}
</script>

<style scoped>
.line-wrap {
  width: 100%;
  height: 400px;
}
</style>
