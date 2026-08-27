<script setup lang="ts">
import {
  Briefcase,
  DataAnalysis,
  DocumentAdd,
  House,
  User,
  Setting,
} from '@element-plus/icons-vue'
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const title = computed(() => String(route.meta.title ?? '招聘信息管理系统'))
const user = ref<{ display_name: string; roles: string[] } | null>(null)
const loading = ref(true)
const error = ref('')
const form = reactive({ username: 'admin', password: '' })

async function loadUser() {
  const response = await fetch('/api/v1/auth/me', { credentials: 'include' })
  if (response.ok) user.value = await response.json()
  loading.value = false
}

async function login() {
  error.value = ''
  const response = await fetch('/api/v1/auth/login', {
    method: 'POST', credentials: 'include', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form),
  })
  if (!response.ok) { error.value = '用户名或密码错误'; return }
  user.value = await response.json()
}

async function logout() {
  await fetch('/api/v1/auth/logout', { method: 'POST', credentials: 'include' })
  user.value = null
  form.password = ''
}

onMounted(() => loadUser().catch(() => { loading.value = false }))

const menuItems = [
  { path: '/', label: '工作台', icon: House },
  { path: '/demands', label: '招聘需求', icon: Briefcase },
  { path: '/candidates', label: '候选人', icon: User },
  { path: '/resume-workloads', label: '简历推荐', icon: DocumentAdd },
  { path: '/dashboard', label: '数据看板', icon: DataAnalysis },
]
const visibleMenuItems = computed(() => user.value?.roles.includes('SYSTEM_ADMIN')
  ? [...menuItems, { path: '/admin', label: '系统管理', icon: Setting }]
  : menuItems)
</script>

<template>
  <div v-if="loading" class="login-screen">加载中...</div>
  <div v-else-if="!user" class="login-screen">
    <el-card class="login-card">
      <h2>招聘信息管理系统</h2>
      <el-form @submit.prevent="login">
        <el-form-item><el-input v-model="form.username" placeholder="用户名" /></el-form-item>
        <el-form-item><el-input v-model="form.password" type="password" show-password placeholder="密码" @keyup.enter="login" /></el-form-item>
        <el-alert v-if="error" :title="error" type="error" :closable="false" />
        <el-button type="primary" native-type="submit" class="login-button">登录</el-button>
      </el-form>
    </el-card>
  </div>
  <el-container v-else class="app-shell">
    <el-aside width="208px" class="app-sidebar">
      <div class="brand">招聘管理</div>
      <el-menu :default-active="route.path" router>
        <el-menu-item v-for="item in visibleMenuItems" :key="item.path" :index="item.path">
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
          <span>{{ user.display_name }}</span>
          <el-button link @click="logout">退出</el-button>
        </div>
      </el-header>
      <el-main class="app-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>
