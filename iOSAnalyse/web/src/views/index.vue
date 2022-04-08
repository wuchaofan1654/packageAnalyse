<template>
  <el-card class="box-card" body-style="height: 100vh">
    <div slot="header" class="clearfix" style="height: 25px">
      <el-col :span="8">
        <header-left :title="title"/>
      </el-col>
      <el-col :span="16" style="text-align: right">
        <div class="handlers" style="width: 240px; float: right">
          <el-container>
            <el-button size="mini" type="success" @click="addPublish">
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
      <el-table-column label="json file" align="center" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-button type="text" @click="downloadJsonfile(scope.row.jsonfile)">点击查看</el-button>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" align="center" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <span size="mini" style="color: #606266">{{ scope.row.create_time }}</span>
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
    <el-dialog
      title="手动上传发布记录"
      :visible.sync="publishDialogVisible"
      width="60%"
      center>
      <el-form ref="form" :model="form" label-width="150px">
        <el-form-item label="App版本">
          <el-input v-model="form.version"></el-input>
        </el-form-item>
        <el-form-item label="jenkins构建编号">
          <el-input v-model="form.build_no"></el-input>
        </el-form-item>
        <el-form-item label="版本分支">
          <el-input v-model="form.branch"></el-input>
        </el-form-item>
        <el-form-item label="包大小json文件">
          <input class="file" name="result" type="file" @change="appendFileToForm"/>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="centerDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitPublishForm">提 交</el-button>
      </span>
    </el-dialog>
  </el-card>
</template>

<script>
import {listPublish, addPublishByFile} from "@/api/publish"
import HeaderLeft from "./HeaderLeft";


export default {
  name: "index",
  components: {HeaderLeft},
  data() {
    return {
      title: 'iOS发布记录',
      versionOptions: [],
      selectList: [],
      publishes: [],
      loading: false,
      total: 0,
      publishDialogVisible: false,
      pageSizes: [10, 20 ,50, 100],
      queryParams: {
        pageNum: 1,
        pageSize: 20
      },
      form: {
        version: '',
        build_no: '',
        branch: '',
        result: ''
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
    addPublish() {
      this.publishDialogVisible = true
      this.$message.success('正在开发中～')
    },
    handleSizeChange(value) {
      this.queryParams.pageSize = value
      this.publishes = this.getList()
    },
    handleCurrentPageChange(value) {
      this.queryParams.pageNum = value
      this.publishes = this.getList()
    },
    appendFileToForm(e) {
      this.form.result = e.target.files[0]
    },
    submitPublishForm() {
      this.publishDialogVisible = false
      console.log(this.form)
      addPublishByFile(this.form).then(res => {
        if(res.code === 200) {
          this.$message.success('发布成功')
        }else {
          this.$message.success('添加失败')
        }
      })
    },
    downloadJsonfile(filepath) {
      console.log(filepath)
      window.open(filepath)
    }
  }
}
</script>

<style scoped>
</style>
