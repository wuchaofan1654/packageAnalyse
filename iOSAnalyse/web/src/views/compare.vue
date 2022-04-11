<template>
  <el-card class="box-card">
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
      <el-table-column
        label="组件名"
        align="center"
        :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-link
            :underline="false"
            @click="getJumpUrl(scope.row.name)">
            {{scope.row.name}}
          </el-link>
        </template>
      </el-table-column>
      <el-table-column
        label="旧版本大小"
        align="center"
        prop="old"
        sortable
        :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-link :type="getVersionValueType(scope.row.old)" :underline="false">
            <span>{{dataFormat(scope.row.old).value}}</span>
            <span>{{dataFormat(scope.row.old).unit}}</span>
          </el-link>
        </template>
      </el-table-column>
      <el-table-column
        label="新版本大小"
        align="center"
        prop="new"
        sortable
        :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-link :type="getVersionValueType(scope.row.new)" :underline="false">
            <span>{{dataFormat(scope.row.new).value}}</span>
            <span>{{dataFormat(scope.row.new).unit}}</span>
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
          <el-link :type="getDiffValueType(scope.row.diff)" :underline="false">
            <span>{{dataFormat(scope.row.diff).value}}</span>
            <span>{{dataFormat(scope.row.diff).unit}}</span>
          </el-link>
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
  mounted() {
    this.getList(this.$route.query.pk1, this.$route.query.pk2)
  },
  methods: {
    getStatus(value) {
      return value > 0 ? 'danger' : 'success'
    },

    getList(pk1, pk2) {
      this.loading = true
      comparePublish(pk1, pk2).then(res => {
        this.loading = false
        if (res.code === 200) {
          this.modules = res.data

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
      }
      else {
        if (Math.abs(data) > 1024) {
          formatted.value = (data / 1024).toFixed(2)
          formatted.unit = 'kb'
        } else {
          formatted.value = data
        }
      }
      return formatted
    },

    getDiffValueType(value) {
      value = this.dataFormat(value)
      return value.value < 0 ? 'success' : value.value === 0 ? 'info' : 'danger'
    },

    getVersionValueType(value) {
      return value > 1024 * 1024 ? 'danger' : value > 1024 ? 'warning': 'info'
    },

    sortDiff(a, b) {
      return a.value - b.value
    },

    getJumpUrl(module_name) {
      return this.$router.push({path: 'module', query: {module_name: module_name}})
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
