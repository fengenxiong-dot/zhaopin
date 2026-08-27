<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <section>
    <div class="page-heading">
      <div>
        <h1>{{ route.meta.title }}</h1>
        <p>{{ route.meta.description }}</p>
      </div>
    </div>
    <el-empty description="该模块将在后续开发阶段接入" />
  </section>
</template>

