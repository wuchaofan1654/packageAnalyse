<template>
  <el-card class="box-card" body-style="height: 100vh">
    <div slot="header" class="clearfix" style="height: 25px">
      <el-col :span="8">
        <header-left :title="title"/>
      </el-col>
      <el-col :span="16" style="text-align: right">
        <div class="handlers" style="width: 240px; float: right">
          <el-container>
            <el-button size="mini" type="success" @click="adPublish">
              上传发布记录
            </el-button>
            <el-button size="mini" type="primary" @click="compare">
              开始对比
            </el-button>
          </el-container>
        </div>
      </el-col>
    </div>
    <el-table
      v-loading="loading"
      ref="multipleTable"
      @select-all="onSelectAll"
      @selection-change="onSelectChange"
      :data="publishes">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="版本号" align="center" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <span>{{ scope.row.version }}</span>
        </template>
      </el-table-column>
      <el-table-column label="build编号" align="center" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <span>{{ scope.row.build_no }}</span>
        </template>
      </el-table-column>
      <el-table-column label="分支名" align="center" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <span size="mini">{{ scope.row.branch }}</span>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" align="center" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <span size="mini" style="color: #606266">{{ scope.row.create_time }}</span>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.pageNum"
      :limit.sync="queryParams.pageSize"
      @pagination="getList"
    />
  </el-card>
</template>

<script>
import {listPublish} from "@/api/publish"
import HeaderLeft from "./HeaderLeft";
import Pagination from "../components/Pagination/index"


export default {
  name: "index",
  components: {HeaderLeft, Pagination},
  data() {
    return {
      title: 'iOS发布记录',
      versionOptions: [],
      selectList: [],
      publishes: [],
      loading: false,
      total: 0,
      queryParams: {
        pageNum: 1,
        pageSize: 20
      }
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
        this.publishes = res.data.results
        this.total = res.data.count
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
    goBack() {
      this.$router.go(-1)
    },
    addPublish() {
      this.$message.success('正在开发中～')
    }
  }
}
</script>

<style scoped>
</style>
