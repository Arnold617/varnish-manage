<template>
  <div class="departContent app-container calendar-list-container">
    <!-- 列表 -->
    <div class="table_content tablecheck">
      <el-table v-loading="listLoading"
                :data="groupList"
                :header-cell-style="{background:'#DFE6EC'}"
                element-loading-text="老板,不等一下吗？"
                border
                fit
                style="width:100%;font-size:13px">
        <el-table-column prop="name" align="center" label="名称"/>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <!-- 编辑界面 -->
    <div class="dialog_color">
      <el-dialog :visible.sync="syncVisible" :close-on-click-modal="false" title="编辑">
        <el-form ref="editForm" :model="editForm" label-width="80px">
          <el-form-item label="用户名" prop="firstname">
            <el-select v-model="editForm.first_name" value-key="id" filterable style="width: 400px">
              <el-option v-for="(item,index) in nameList" :key="index" :label="item.first_name" :value="item.first_name"/>
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="syncVisible = false">取消</el-button>
          <el-button :loading="editLoading" type="primary" @click.native="editSubmit">提交</el-button>
        </div>
      </el-dialog>
    </div>

  </div>
</template>

<script>
import moment from 'moment-timezone'
import { getUserList, getGroupList } from '@/api/api'

export default {
  data() {
    return {
      groupList: [],
      listLoading: false,
      editLoading: false,
      tableQuery: {},
      syncVisible: false,
      // 编辑界面数据
      editForm: {
        id: 0,
        first_name: ''
      },
      nameList: []
    }
  },
  created() {
    this.get_groupList()
    this.get_nameList()
  },
  methods: {
    get_groupList() {
      this.listLoading = true
      getGroupList()
        .then(res => {
          this.groupList = res.data.data
          // console.log(res.data.data)
          this.listLoading = false
        })
    },  
    get_nameList() {
      getUserList()
        .then(res => {
          this.nameList = res.data.data
          // console.log(res.data)
        })
    },
    // 显示编辑界面
    handleEdit(row) {
      this.syncVisible = true
      this.editForm = Object.assign({}, row)
    },
    // 删除
    handleDelete(row) {
      this.$confirm('确认删除该域名吗?', '提示', {
        type: 'warning'
      }).then(() => {
        this.listLoading = true
        deleteDel('/api/proxy/uvarnish/group/' + row.id)
          .then((res) => {
            this.listLoading = false
            // NProgress.done();
            this.$message({
              message: '删除成功',
              type: 'success'
            })
            this.get_groupList()
          })
      }).catch(() => {})
    },
    // 编辑
    editSubmit() {
      this.$refs.editForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            this.editLoading = true
            // NProgress.start();
            const para = Object.assign({}, this.editForm)
            const url = '/api/proxy/uvarnish/user/'
            postAdd(url, para)
              .then((res) => {
                this.editLoading = false
                this.$message({
                  message: '提交成功',
                  type: 'success'
                })
                this.$refs['editForm'].resetFields()
                this.syncVisible = false
                this.get_groupList()
              })
          })
        }
      })
    }

  }
}
</script>

<style>
</style>
