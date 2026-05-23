<template>
  <div class="teacher-home">
    <div class="header">
      <h1>教师中心</h1>
      <p class="subtitle">智能教学助手，让教学更高效</p>
    </div>
    
    <div class="function-grid">
      <!-- 备课与设计 -->
      <el-card class="function-card design-card" shadow="hover" @click="$router.push('/teacher/design')">
        <div class="card-content">
          <div class="icon-wrapper design-icon">
            <el-icon size="48"><Document /></el-icon>
          </div>
          <h3>备课与设计</h3>
          <p class="description">AI智能生成教学内容，包括知识讲解、实训练习与时间分布</p>
          <div class="features">
            <span class="feature-tag">课程大纲</span>
            <span class="feature-tag">知识讲解</span>
            <span class="feature-tag">实训指导</span>
          </div>
        </div>
      </el-card>

      <!-- 考核内容生成 -->
      <el-card class="function-card assessment-card" shadow="hover" @click="$router.push('/teacher/assessment')">
        <div class="card-content">
          <div class="icon-wrapper assessment-icon">
            <el-icon size="48"><EditPen /></el-icon>
          </div>
          <h3>考核内容生成</h3>
          <p class="description">根据教学内容自动生成多样化考核题目及参考答案</p>
          <div class="features">
            <span class="feature-tag">试题生成</span>
            <span class="feature-tag">参考答案</span>
            <span class="feature-tag">难度分级</span>
          </div>
        </div>
      </el-card>

      <!-- 学情数据分析 -->
      <el-card class="function-card analytics-card" shadow="hover" @click="$router.push('/teacher/analytics')">
        <div class="card-content">
          <div class="icon-wrapper analytics-icon">
            <el-icon size="48"><TrendCharts /></el-icon>
          </div>
          <h3>学情数据分析</h3>
          <p class="description">智能分析学生学习数据，提供个性化教学建议</p>
          <div class="features">
            <span class="feature-tag">学习分析</span>
            <span class="feature-tag">错误定位</span>
            <span class="feature-tag">教学建议</span>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { Document, EditPen, TrendCharts } from '@element-plus/icons-vue'
</script>

<style scoped>
.teacher-home {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px 20px;
}

.header {
  text-align: center;
  margin-bottom: 60px;
  color: white;
}

.header h1 {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 16px;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  margin: 0;
}

.function-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.function-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 16px;
  border: none;
  background: white;
  min-height: 280px;
}

.function-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.1) !important;
}

.card-content {
  text-align: center;
  padding: 30px 20px;
}

.icon-wrapper {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: white;
}

.design-icon {
  background: linear-gradient(135deg, #4CAF50, #45a049);
}

.assessment-icon {
  background: linear-gradient(135deg, #2196F3, #1976D2);
}

.analytics-icon {
  background: linear-gradient(135deg, #FF9800, #F57C00);
}

.card-content h3 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 12px;
  color: #333;
}

.description {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 20px;
}

.features {
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

.feature-tag {
  background: #f0f2f5;
  color: #666;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.design-card .feature-tag {
  background: #e8f5e8;
  color: #4CAF50;
}

.assessment-card .feature-tag {
  background: #e3f2fd;
  color: #2196F3;
}

.analytics-card .feature-tag {
  background: #fff3e0;
  color: #FF9800;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .function-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .header h1 {
    font-size: 2.5rem;
  }
  
  .teacher-home {
    padding: 20px 15px;
  }
}
</style> 