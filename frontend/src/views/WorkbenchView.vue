<script setup lang="ts">
const metrics = [
  { label: '招聘中需求', value: 0, note: '等待创建招聘需求' },
  { label: '进行中候选人', value: 0, note: '合格简历建档后显示' },
  { label: '今日面试', value: 0, note: '暂无待面试安排' },
  { label: '近期待报到', value: 0, note: '未来14天' },
]
</script>

<template>
  <section>
    <div class="page-heading">
      <div>
        <h1>欢迎使用招聘信息管理系统</h1>
        <p>系统骨架已就绪，下一阶段将接入用户、权限与业务数据。</p>
      </div>
    </div>

    <el-row :gutter="16">
      <el-col v-for="metric in metrics" :key="metric.label" :xs="12" :sm="12" :lg="6">
        <el-card shadow="never" class="metric-card">
          <div class="metric-label">{{ metric.label }}</div>
          <div class="metric-value">{{ metric.value }}</div>
          <div class="metric-note">{{ metric.note }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card shadow="never" class="status-card">
      <template #header>
        <strong>阶段 0 状态</strong>
      </template>
      <el-result icon="success" title="工程基础已建立" sub-title="后端、前端、数据库和统一入口已完成配置。" />
    </el-card>
  </section>
</template>

