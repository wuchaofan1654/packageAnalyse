<template>
  <div style="font-size: 16px">
    <el-button type="text" @click="goHomePage" icon="el-icon-s-home">首页</el-button>
    <el-divider direction="vertical" />
    <el-button type="text" @click="goBack">🔙上一页</el-button>
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
    goBack() {
      this.$router.go(-1)
    },
  }
}
</script>

<style scoped>

</style>
