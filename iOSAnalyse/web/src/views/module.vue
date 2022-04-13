<template>
  <el-card class="box-card">
    <div slot="header" class="clearfix">
      <el-row :gutter="22">
        <el-col :span="8">
        <header-left :title="title" />
      </el-col>
      <el-col :span="16" style="text-align: right">
        <el-input
            size="mini"
            style="width: 200px"
            v-model="queryParams.version"
            @blur="getList"
            clearable
            prefix-icon="el-icon-search"
            placeholder="支持输入版本号过滤～"/>
        <el-select
          size="mini"
          v-model="queryParams.module_name"
          filterable
          clearable
          placeholder="选择组件后可查看趋势图～"
          @change="getList">
          <el-option
            v-for="item in moduleNameOptions"
            :key="item.id"
            :label="item.name"
            :value="item.name"/>
        </el-select>
        <el-divider v-if="queryParams.module_name" direction="vertical"/>
        <el-button
          v-if="queryParams.module_name"
          size="mini"
          type="primary"
          @click="showExtend">
          查看走势图</el-button>
      </el-col>
      </el-row>
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
          <el-tag size="mini" type="info">{{scope.row.publish.version}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="组件大小" align="center" :show-overflow-tooltip="true">
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
          <el-tag size="mini" type="primary">{{scope.row.publish.build_no}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" align="center" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <span size="mini" style="color: #606266; font-size: 12px">
             <i class="el-icon-time"/>
            {{scope.row.create_time}}
          </span>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog
      :title="title"
      :visible.sync="dialogVisible"
      width="60%"
      center>
      <module-chart :modules="modules" v-if="dialogVisible"></module-chart>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible=false">取 消</el-button>
        <el-button type="primary" @click="dialogVisible=false">确 定</el-button>
      </span>
    </el-dialog>
     <el-pagination
      style="text-align: center; margin: 20px"
      :total="total"
      :page-size="queryParams.pageSize"
      :current-page="queryParams.pageNum"
      :page-sizes="pageSizes"
      :background="true"
      layout="total, sizes, prev, pager, next, jumper"
      @size-change="handleSizeChange"
      @current-change="handleCurrentPageChange"
    />
  </el-card>
</template>

<script>
import {listModule, get_module_options} from "@/api/module"
import moduleChart from "./moduleChart";
import HeaderLeft from "./HeaderLeft";

export default {
  components: {
    moduleChart,
    HeaderLeft,
  },
name: "index",
  data() {
  return {
    title: '模块各版本大小',
    total: 0,
    moduleNameOptions: [],
    pageSizes: [10, 20, 50, 100],
    queryParams: {
      pageNum: 1,
      pageSize: 20,
      module_name: '',
      version: ''
    },
    modules: [],
    dialogVisible: false,
    chart_title: '走势图'
    }
  },
  watch: {

  },
  created() {
    this.queryParams.module_name = this.$route.query.module_name
    this.getModuleOptions()
    this.getList()
  },
  methods: {
    getStatus(value) {
      return value > 0 ? 'danger' : 'success'
    },
    getList() {
      listModule(this.queryParams).then(res => {
        if (res.code === 200) {
          this.modules = res.data.results
          this.total = res.data.count
        } else {
          this.modules = []
          this.$message.error('接口数据异常，请稍后再试～')
        }
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
          if (res.code === 200) {
            this.moduleNameOptions = res.data
            this.total = res.data.count
          } else {
            this.moduleNameOptions = []
          }
      })
    },
    showExtend() {
      this.dialogVisible = true
    },
    handleSizeChange(value) {
      this.queryParams.pageSize = value
      this.publishes = this.getList()
    },
    handleCurrentPageChange(value) {
      this.queryParams.pageNum = value
      this.publishes = this.getList()
    },
  }
}
</script>

<style scoped>
.box-card {
  overflow: auto;
  max-height: 100vh;
  padding: 5px;
}

.box-card::-webkit-scrollbar {
  display: none;
}
</style>
