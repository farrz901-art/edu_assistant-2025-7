<template>
  <div class="knowledge-chart">
    <el-empty v-if="!data || data.length === 0" description="暂无数据" />
    <div v-else class="chart-container">
      <h3>知识点掌握情况</h3>
      <div class="chart"></div>
    </div>
  </div>
</template>

<script>
// import { onMounted, watch } from 'vue'

import {watch} from "vue";

export default {
  props: {
    data: Array
  },
  setup(props) {
    // 模拟图表渲染
    const renderChart = () => {
      console.log('渲染知识点图表', props.data)
    }

    watch(() => props.data, (newData) => {
      if (newData && newData.length > 0) {
        renderChart()
      }
    }, { immediate: true })

    return {}
  }
}
</script>