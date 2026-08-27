<script setup lang="ts">
import {
  Briefcase,
  DataAnalysis,
  DocumentAdd,
  House,
  User,
} from '@element-plus/icons-vue'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const title = computed(() => String(route.meta.title ?? '招聘信息管理系统'))

const menuItems = [
  { path: '/', label: '工作台', icon: House },
  { path: '/demands', label: '招聘需求', icon: Briefcase },
  { path: '/candidates', label: '候选人', icon: User },
  { path: '/resume-workloads', label: '简历推荐', icon: DocumentAdd },
  { path: '/dashboard', label: '数据看板', icon: DataAnalysis },
]
</script>

<template>
  <el-container class="app-shell">
    <el-aside width="208px" class="app-sidebar">
      <div class="brand">招聘管理</div>
      <el-menu :default-active="route.path" router>
        <el-menu-item v-for="item in menuItems" :key="item.path" :index="item.path">
          <el-icon><component :is="item.icon" /></el-icon>
          <span>{{ item.label }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="app-header">
        <strong>{{ title }}</strong>
        <div class="current-user">
          <el-avatar :size="32">管</el-avatar>
          <span>系统管理员</span>
        </div>
      </el-header>
      <el-main class="app-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

