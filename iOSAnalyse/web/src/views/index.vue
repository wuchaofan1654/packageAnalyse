<template>
  <el-container>
    <el-header height="42px" style="background-color: #baf6db">
      <el-row :gutter="22">
        <el-col :span="12">
          <top-bar :title="title"/>
        </el-col>
        <el-col :span="12">
          <div class="class-options">
            <el-input
              size="mini"
              style="width: 200px"
              v-model="queryParams.version"
              @blur="getList"
              prefix-icon="el-icon-search"
              placeholder="支持输入版本号过滤～"/>
            <el-divider direction="vertical"/>
            <el-button size="mini" type="primary" @click="compare">
              开始对比
            </el-button>
          </div>
        </el-col>
      </el-row>
    </el-header>
    <el-main>
      <el-table
        v-loading="loading"
        ref="multipleTable"
        @select-all="onSelectAll"
        @selection-change="onSelectChange"
        :data="publishes">
        <el-table-column type="selection" width="55" align="center"/>
        <el-table-column
          label="版本号"
          align="center"
          prop="version"
          sortable
          :show-overflow-tooltip="true">
        </el-table-column>
        <el-table-column
          label="build编号"
          align="center"
          sortable
          prop="build_no"
          :show-overflow-tooltip="true">
        </el-table-column>
        <el-table-column
          label="分支名"
          align="center"
          sortable
          prop="branch"
          :show-overflow-tooltip="true">
        </el-table-column>
        <el-table-column
          label="Json-file"
          align="center"
          :show-overflow-tooltip="true">
          <template slot-scope="scope">
            <el-tooltip :content="scope.row.jsonfile" placement="top">
              <el-button type="text" @click="downloadJsonfile(scope.row.jsonfile)">
                点击查看
              </el-button>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column
          label="创建时间"
          align="center"
          :show-overflow-tooltip="true">
          <template slot-scope="scope">
          <span size="mini" style="color: #606266; font-size: 12px">
            <i class="el-icon-time"/>
            {{ scope.row.create_time }}</span>
          </template>
        </el-table-column>
      </el-table>
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
    </el-main>
  </el-container>
</template>

<script>
import {listPublish} from "@/api/publish"
import topBar from "./topBar";


export default {
  name: "index",
  components: {topBar},
  data() {
    return {
      title: 'iOS发布记录',
      versionOptions: [],
      selectList: [],
      publishes: [],
      loading: false,
      total: 0,
      filterText: '',
      publishDialogVisible: false,
      pageSizes: [10, 20, 50, 100],
      queryParams: {
        pageNum: 1,
        pageSize: 20,
        version: ''
      },
      form: {}
    }
  },
  created() {
    this.getList()
  },
  watch: {},
  methods: {
    getList() {
      this.loading = true
      this.seleted = []
      listPublish().then(res => {
        this.loading = false
        if (res.code === 200) {
          this.publishes = res.data.results
          this.total = res.data.count
        } else {
          this.publishes = []
          this.$message.error('接口数据异常，请稍后再试～')
        }
      })
    },
    compare() {
      if (this.selectList.length < 2) {
        this.$message.error('请选择2条记录进行对比~')
        return
      }
      this.$router.push(
        {
          path: 'compare',
          query: {
            pk1: this.selectList[0]['id'],
            pk2: this.selectList[1]['id']
          }
        }
      )
    },
    onSelectAll() {
      this.$message.error('暂时只支持2条记录对比，不支持全选功能～')
      this.$refs.multipleTable.clearSelection()
    },
    onSelectChange(rows) {
      if (rows.length > 2) {
        this.$refs.multipleTable.toggleRowSelection(rows[0], false);
        rows.splice(0, 1);//同时要把选中第一项移除
      }
      this.selectList = rows;
    },
    addPublish() {
      this.publishDialogVisible = true
    },
    handleSizeChange(value) {
      this.queryParams.pageSize = value
      this.publishes = this.getList()
    },
    handleCurrentPageChange(value) {
      this.queryParams.pageNum = value
      this.publishes = this.getList()
    },
    getJumpUrl(version) {
      return this.$router.push({path: 'module', query: {version: version}})
    },
    downloadJsonfile(filepath) {
      window.open(filepath)
    },
  }
}
</script>

<style scoped>
.class-options {
  text-align: right;
}
</style>
