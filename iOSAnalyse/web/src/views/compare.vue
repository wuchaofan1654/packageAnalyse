<template>
  <el-card class="box-card" body-style="height: 100vh">
    <div slot="header" class="clearfix" style="height: 25px">
      <el-col :span="8">
        <header-left :title="title" />
      </el-col>
      <el-col :span="16" style="text-align: right">
      </el-col>
    </div>
    <el-table
      v-loading="loading"
      :data="modules">
      <el-table-column label="组件名" align="center" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-link :underline="false" @click="getJumpUrl(scope.row.name)">{{scope.row.name}}</el-link>
        </template>
      </el-table-column>
      <el-table-column label="旧版本大小" align="center" prop="old" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.old > 1024 * 1024" size="mini" type="danger">{{dataFormat(scope.row.old)}}</el-tag>
          <el-tag v-else-if="scope.row.old > 0.2 * 1024" size="mini" type="warning">{{dataFormat(scope.row.old)}}</el-tag>
          <el-tag v-else size="mini">{{dataFormat(scope.row.old)}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="新版本大小" align="center" prop="new" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.new > 1024 * 1024" size="mini" type="danger">{{dataFormat(scope.row.new)}}</el-tag>
          <el-tag v-else-if="scope.row.new > 0.2 * 1024" size="mini" type="warning">{{dataFormat(scope.row.new)}}</el-tag>
          <el-tag v-else size="mini">{{dataFormat(scope.row.new)}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="差值" align="center" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.diff > 0" size="mini" type="danger">上升 {{dataFormat(scope.row.diff)}}</el-tag>
          <el-tag v-else-if="scope.row.diff < 0" size="mini" type="success">下降 {{dataFormat(scope.row.diff)}}</el-tag>
          <el-tag v-else size="mini">0 b</el-tag>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script>
import {comparePublish} from "@/api/publish"
import HeaderLeft from "./HeaderLeft";

export default {
  components: {
    HeaderLeft
  },
name: "index",
  data() {
  return {
    title: '对比结果',
    versionOptions: [],
    modules: [],
    loading: false
    }
  },
  created() {
  this.getList()
  },
  methods: {
    getStatus(value) {
      return value > 0 ? 'danger' : 'success'
    },
    getList() {
      this.loading = true
      comparePublish(1, 2).then(res => {

        this.loading = false
        this.modules = res.data
      })
    },
    dataFormat(data) {
      if (Math.abs(data) > 1024 * 1024) {
        return (data / (1024 * 1024)).toFixed(1) + ' mb'
      }
      else {
        if (Math.abs(data) > 1024) {
          return (data / 1024).toFixed(1) + ' kb'
        }
        else {
          return data + ' b'
        }
      }
    },
    getJumpUrl(module_name) {
      return this.$router.push({path: 'module', query: {module_name: module_name}})
    },
  }
}
</script>

<style scoped>

</style>
