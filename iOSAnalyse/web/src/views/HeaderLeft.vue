<template>
  <div style="font-size: 16px">
    <el-button type="text" @click="goHomePage">
      <span>首页</span>
    </el-button>
    <el-divider direction="vertical" />
    <span>{{ title }}</span>
  </div>
</template>

<script>
export default {
  name: "HeaderLeft",
  props: {
    title: {      //父组件传过来的值
      type: String
    }
  },
  methods: {
    goHomePage() {
      this.$router.push({path: '/'})
    },
  }
}
</script>

<style scoped>

</style>
