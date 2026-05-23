<template>
  <el-card shadow="hover" class="stat-card">
    <div class="card-content">
      <div class="icon" :style="{ backgroundColor: color + '20', color: color }">
        <el-icon :size="24">
          <component :is="icon" />
        </el-icon>
      </div>
      <div class="text">
        <div class="value">{{ value }}</div>
        <div class="title">{{ title }}</div>
      </div>
    </div>
  </el-card>
</template>

<script>
export default {
  props: {
    title: String,
    value: [Number, String],
    icon: String,
    color: {
      type: String,
      default: '#409EFF'
    }
  }
}
</script>

<style scoped>
.stat-card {
  margin-bottom: 20px;
}
.card-content {
  display: flex;
  align-items: center;
}
.icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
}
.text {
  line-height: 1.5;
}
.value {
  font-size: 24px;
  font-weight: bold;
}
.title {
  color: #999;
  font-size: 14px;
}
</style>