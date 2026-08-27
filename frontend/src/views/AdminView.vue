<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'

type User = { id: string; username: string; display_name: string; status: string; roles: string[] }
const users = ref<User[]>([])
const visible = ref(false)
const form = reactive({ username: '', display_name: '', password: '', role_codes: ['HR'] })
const roleOptions = [
  { label: '普通 HR', value: 'HR' },
  { label: '招聘管理者', value: 'RECRUITMENT_MANAGER' },
  { label: '系统管理员', value: 'SYSTEM_ADMIN' },
]

async function load() {
  const response = await fetch('/api/v1/users', { credentials: 'include' })
  if (!response.ok) throw new Error('加载失败')
  users.value = await response.json()
}
async function createUser() {
  const response = await fetch('/api/v1/users', { method: 'POST', credentials: 'include',
    headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) })
  if (!response.ok) { ElMessage.error((await response.json()).detail ?? '创建失败'); return }
  visible.value = false; Object.assign(form, { username: '', display_name: '', password: '', role_codes: ['HR'] })
  ElMessage.success('用户已创建'); await load()
}
async function toggle(user: User) {
  await fetch(`/api/v1/users/${user.id}`, { method: 'PATCH', credentials: 'include',
    headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ status: user.status === 'active' ? 'disabled' : 'active' }) })
  await load()
}
onMounted(load)
</script>

<template>
  <el-card>
    <template #header><div class="section-title"><strong>用户管理</strong><el-button type="primary" @click="visible=true">新建用户</el-button></div></template>
    <el-table :data="users">
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="display_name" label="姓名" />
      <el-table-column label="角色"><template #default="scope">{{ scope.row.roles.join('、') }}</template></el-table-column>
      <el-table-column label="状态"><template #default="scope"><el-tag :type="scope.row.status==='active'?'success':'info'">{{ scope.row.status==='active'?'启用':'停用' }}</el-tag></template></el-table-column>
      <el-table-column label="操作"><template #default="scope"><el-button link @click="toggle(scope.row)">{{ scope.row.status==='active'?'停用':'启用' }}</el-button></template></el-table-column>
    </el-table>
  </el-card>
  <el-dialog v-model="visible" title="新建用户" width="460px">
    <el-form label-width="80px"><el-form-item label="用户名"><el-input v-model="form.username" /></el-form-item>
      <el-form-item label="姓名"><el-input v-model="form.display_name" /></el-form-item>
      <el-form-item label="初始密码"><el-input v-model="form.password" type="password" show-password /></el-form-item>
      <el-form-item label="角色"><el-select v-model="form.role_codes" multiple style="width:100%"><el-option v-for="r in roleOptions" :key="r.value" :label="r.label" :value="r.value" /></el-select></el-form-item></el-form>
    <template #footer><el-button @click="visible=false">取消</el-button><el-button type="primary" @click="createUser">创建</el-button></template>
  </el-dialog>
</template>
