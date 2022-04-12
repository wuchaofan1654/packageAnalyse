<template>
  <el-card class="box-card">
    <div slot="header" class="clearfix">
      <el-row>
        <el-col :span="12">
          <header-left :title="title"/>
        </el-col>
        <el-col :span="12" style="text-align: right">
          <el-input
            size="mini"
            style="width: 200px"
            v-model="filterText"
            @input="filterVersion"
            prefix-icon="el-icon-search"
            placeholder="支持输入版本号过滤～"/>
          <el-divider direction="vertical" />
          <el-button size="mini" type="primary" @click="compare">
            开始对比
          </el-button>
        </el-col>
      </el-row>
    </div>
    <el-table
      v-loading="loading"
      ref="multipleTable"
      @select-all="onSelectAll"
      @selection-change="onSelectChange"
      :data="filtered">
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
      <el-table-column label="Json-file" align="center" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-button type="text" @click="downloadJsonfile(scope.row.jsonfile)">点击查看</el-button>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" align="center" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <span size="mini" style="color: #606266">
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
          <el-input class="file" name="jsonfile" v-model="form.jsonfile" type="file"/>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="publishDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitPublishForm">提 交</el-button>
      </span>
    </el-dialog>
  </el-card>
</template>

<script>
import {listPublish, addPublish} from "@/api/publish"
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
      filtered: [],
      loading: false,
      total: 0,
      filterText: '',
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
        jsonfile: ''
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
        if (res.code === 200) {
          this.publishes = this.filtered = res.data.results
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
    submitPublishForm() {
      this.publishDialogVisible = false
      addPublish(this.form).then(res => {
        console.log(this.form)
        if(res.code === 200) {
          console.log(res)
          this.$message.success('发布成功')
        }else {
          this.$message.success('添加失败')
        }
      })
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
    filterVersion() {
      let filterText = this.filterText
      this.filtered = this.publishes.filter(function (publish) {
        return publish.version.indexOf(filterText) !== -1;
      });
    }
  }
}
</script>

<style scoped>
</style>
