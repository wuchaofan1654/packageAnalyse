<template>
  <div style="font-size: 16px">
    <el-dropdown type="text">
      <el-button type="text">
        <i class="el-icon-menu"/>
        导航菜单
      </el-button>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item v-for="menu in menus" :key="menu.title">
          <el-link
            :icon="menu.icon"
            :href="menu.route">
            {{menu.title}}
          </el-link>
        </el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
    <el-divider direction="vertical" />
    <el-button type="text" @click="goBack">🔙上一页</el-button>
    <el-divider direction="vertical" />
    <span>{{ title }}</span>
  </div>
</template>

<script>
export default {
  name: "HeaderLeft",
  data () {
    return {
      menus: [
        {title: '发布列表', icon: 'el-icon-s-home', route: '/v1'},
        {title: '模块列表', icon: 'el-icon-s-data', route: '/v1/module'}
      ]
    }
  },
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
