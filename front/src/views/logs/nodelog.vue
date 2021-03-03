<template>
  <div class="departContent app-container calendar-list-container">
    <!-- 工具条 -->
    <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="filters">
				<el-form-item>
					<el-input v-model="filters.name" style="width: 300px" placeholder="模糊匹配"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" v-on:click="get_logsList">查询</el-button>
				</el-form-item>
			</el-form>
		</el-col>
    <!-- 列表 -->
    <div class="table_content tablecheck">
      <el-table v-loading="listLoading"
                :data="logList"
                :header-cell-style="{background:'#DFE6EC'}"
                element-loading-text="老板,不等一下吗？"
                border
                fit
                style="width:100%;font-size:13px">
        <el-table-column type="index" label="ID" width="100px" align="center"/>
        <el-table-column prop="name" label="名称" align="center"/>
        <el-table-column prop="room" label="机房" align="center"/>
        <el-table-column :show-overflow-tooltip="true" prop="ip" label="节点ip" align="center"/>
        <el-table-column label="操作用户" align="center">
          <template slot-scope="scope">
            {{ scope.row.user_displayname+'('+scope.row.username+')' }}
          </template>
        </el-table-column>
        <el-table-column label="类型" align="center">
          <template slot-scope="scope">
            {{ scope.row.history_type|typeFilter }}
          </template>
        </el-table-column>
        <el-table-column label="操作时间" align="center">
          <template slot-scope="scope">
            {{ scope.row.history_date|parseDate }}
          </template>
        </el-table-column>
      </el-table>
      <div v-if="!listLoading" class="pagination-container">
        <el-pagination :current-page.sync="page"
                       :page-size="limit"
                       :total="total"
                       layout="total,prev,pager,next,jumper"
                       @size-change="handleSizeChange"
                       @current-change="handleCurrentChange" />
      </div>
    </div>

  </div>
</template>

<script>
import moment from 'moment-timezone'
import { getNodelog } from '@/api/api'

export default {
  filters: {
    typeFilter(val) {
      const types = {
        '+': 'CREAT',
        '~': 'UPDATE',
        '-': 'DELETE'
      }
      return types[val]
    },
    parseDate(val) {
      if (val != '' && val) {
        return moment(val).format('YYYY-MM-DD HH:mm:ss')
      }
    }

  },
  data() {
    return {
      filters: {
        name: ''
      },
      logList: [],
      listLoading: false,
      limit: 15,
      page: 1

    }
  },
  created() {
    this.get_logsList()
  },

  methods: {
    get_logsList() {
      const params = {
        page: this.page,
        name: this.filters.name
      }
      this.listLoading = true
      getNodelog(params)
        .then(res => {
          this.logList = res.data.data
          this.total = res.data.count
          this.listLoading = false
        })
    },
    // 搜索
    handleFilter() {
      this.get_logsList()
    },
    handleSizeChange(val) {
      this.limit = val
      this.page = 1
      this.get_logsList()
    },
    handleCurrentChange(val) {
      this.page = val
      this.get_logsList()
    }

  }
}
</script>

<style>
</style>