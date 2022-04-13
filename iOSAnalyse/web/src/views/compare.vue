<template>
  <el-container>
    <el-header height="42px" style="background-color: #baf6db">
      <el-row :gutter="22">
        <el-col :span="12">
          <top-bar :title="title"/>
        </el-col>
        <el-col :span="12" style="text-align: right">
          <el-input
            size="mini"
            style="width: 200px"
            v-model="filterText"
            @input="filterModuleName"
            prefix-icon="el-icon-search"
            placeholder="支持输入模块名称过滤～"/>
        </el-col>
      </el-row>
    </el-header>
    <el-main>
      <el-table
      v-loading="loading"
      :data="filtered">
      <el-table-column
        label="组件名"
        align="center"
        :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-link
            :underline="false"
            @click="getJumpUrl(scope.row.module_name)">
            {{ scope.row.module_name }}
          </el-link>
        </template>
      </el-table-column>
      <el-table-column
        :label="labels.pk1"
        align="center"
        sortable
        :sort-method="sortModuleSize"
        :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-link :type="getVersionValueType(scope.row.pk1_module_size)" :underline="false">
            <span>{{ dataFormat(scope.row.pk1_module_size).value }}</span>
            <span>{{ dataFormat(scope.row.pk1_module_size).unit }}</span>
          </el-link>
        </template>
      </el-table-column>
      <el-table-column
        :label="labels.pk2"
        align="center"
        sortable
        :sort-method="sortModuleSize"
        :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-link :type="getVersionValueType(scope.row.pk2_module_size)" :underline="false">
            <span>{{ dataFormat(scope.row.pk2_module_size).value }}</span>
            <span>{{ dataFormat(scope.row.pk2_module_size).unit }}</span>
          </el-link>
        </template>
      </el-table-column>
      <el-table-column
        label="差值"
        align="center"
        sortable
        :sort-method="sortDiff"
        :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-link
            :type="formatDiffValue(scope.row.diff_size).type"
            :icon="formatDiffValue(scope.row.diff_size).icon"
            :underline="false">
            <span>{{ dataFormat(scope.row.diff_size).value }}</span>
            <span>{{ dataFormat(scope.row.diff_size).unit }}</span>
          </el-link>
        </template>
      </el-table-column>
    </el-table>
    </el-main>
  </el-container>
</template>

<script>
import {comparePublish} from "@/api/publish"
import topBar from "./topBar";

export default {
  components: {
    topBar
  },
  name: "index",
  data() {
    return {
      title: '对比结果',
      modules: [],
      filtered: [],
      loading: false,
      filterText: '',
      labels: {pk1: '', pk2: ''}
    }
  },
  created() {
    this.getList(this.$route.query.pk1, this.$route.query.pk2)
  },
  methods: {
    getStatus(value) {
      return value > 0 ? 'danger' : 'success'
    },

    async getList(pk1, pk2) {
      this.loading = true
      await comparePublish(pk1, pk2).then(res => {
        this.loading = false
        if (res.code === 200) {
          this.labels.pk1 = res.data.pk1_publish.version + '(' + res.data.pk1_publish.build_no + ')'
          this.labels.pk2 = res.data.pk2_publish.version + '(' + res.data.pk2_publish.build_no + ')'
          this.modules = this.filtered = res.data.results
        } else {
          this.modules = []
          this.$message.error('接口错误，请稍后再试～')
        }
      })
    },
    dataFormat(data) {
      const formatted = {
        value: 0,
        unit: 'b'
      }

      if (!data) {
        return formatted
      }
      if (Math.abs(data) > 1024 * 1024) {
        formatted.value = (data / (1024 * 1024)).toFixed(2)
        formatted.unit = 'mb'
      } else {
        if (Math.abs(data) > 1024) {
          formatted.value = (data / 1024).toFixed(2)
          formatted.unit = 'kb'
        } else {
          formatted.value = data
        }
      }
      return formatted
    },

    formatDiffValue(value) {
      value = this.dataFormat(value)
      return value.value < 0 ? {type: 'success', icon: 'el-icon-bottom'}
      : value.value > 0 ? {type: 'danger', icon: 'el-icon-top'} : {type: 'info', icon: 'el-icon-minus'}
    },

    getVersionValueType(value) {
      return value > 1024 * 1024 ? 'danger' : value > 1024 ? 'warning' : 'info'
    },

    sortModuleSize(a, b) {
      return a.value - b.value
    },

    sortDiff(a, b) {
      return a.value - b.value
    },

    getJumpUrl(module_name) {
      return this.$router.push({path: 'module', query: {module_name: module_name}})
    },
    filterModuleName() {
      let filterText = this.filterText
      this.filtered = this.modules.filter(function (module) {
        return module.module_name.indexOf(filterText) !== -1;
      });
    }
  }
}
</script>

<style scoped>
</style>
