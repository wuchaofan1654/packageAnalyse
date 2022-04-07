<template>
  <el-card class="box-card" body-style="height: 100vh">
    <div slot="header" class="clearfix" style="height: 25px">
      <el-col :span="8">
        <el-button type="text" @click="goHomePage">
          <span style="font-size: 16px">首页</span>
        </el-button>
        <el-divider direction="vertical" />
        <span style="font-size: 16px">模块各版本大小</span>
      </el-col>
      <el-col :span="16" style="text-align: right">
        <el-select
          size="mini"
          v-model="queryParams.module_name"
          placeholder="请选择任一组件"
          @change="getList">
          <el-option
            v-for="item in moduleNameOptions"
            :key="item.id"
            :label="item.name"
            :value="item.name"/>
        </el-select>
        <el-divider v-if="queryParams.module_name" direction="vertical"></el-divider>
        <el-button
          v-if="queryParams.module_name"
          size="mini"
          type="primary"
          @click="showExtend">
          查看走势图</el-button>
      </el-col>
    </div>
    <el-table
      :data="modules">
      <el-table-column label="组件名" align="center" sortable :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <span>{{scope.row.module_name}}</span>
        </template>
      </el-table-column>
      <el-table-column label="版本号" align="center" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <div v-for="publish in scope.row.publish">
            <el-tag size="mini" type="warning">{{publish.version}}</el-tag>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="组件大小" align="center" sortable :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.module_size > 1024 * 1024" size="mini" type="danger">
            {{dataFormat(scope.row.module_size)}}
            </el-tag>
          <el-tag v-else-if="scope.row.module_size > 0.2 * 1024" size="mini" type="warning">
            {{dataFormat(scope.row.module_size)}}
           </el-tag>
          <el-tag v-else size="mini">{{dataFormat(scope.row.module_size)}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="build No." align="center" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <div v-for="publish in scope.row.publish">
            <el-tag size="mini" type="warning">{{publish.build_no}}</el-tag>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" align="center" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <span size="mini" style="color: #606266">{{scope.row.create_time}}</span>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog
      :title="title"
      :visible.sync="dialogVisible"
      width="60%"
      center>
      <module-chart :modules="modules"></module-chart>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible=false">取 消</el-button>
        <el-button type="primary" @click="dialogVisible=false">确 定</el-button>
      </span>
    </el-dialog>
  </el-card>
</template>

<script>
import {listModule, get_module_options} from "@/api/module"
import moduleChart from "./moduleChart";

export default {
  components: {
    moduleChart
  },
name: "index",
  data() {
  return {
    total: 0,
    moduleNameOptions: [],
    queryParams: {
      pageNum: 1,
      pageSize: 100,
      module_name: undefined,
    },
    modules: [],
    dialogVisible: false,
    title: '走势图'
    }
  },
  created() {
    this.queryParams.module_name = this.$route.params.module_name
    this.getModuleOptions()
    this.getList()
  },
  methods: {
    getStatus(value) {
      return value > 0 ? 'danger' : 'success'
    },
    getList() {
      listModule(this.queryParams).then(res => {
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
    getModuleOptions() {
      get_module_options().then(
        res => {
          this.moduleNameOptions = res.data
      })
    },
    showExtend() {
      this.dialogVisible = true
      this.title = this.queryParams.module_name + '走势图'
    },
    goBack() {
      this.$router.go(-1)
    },
    goHomePage() {
      this.$router.push({path: '/'})
    },
  }
}
</script>

<style scoped>

</style>
