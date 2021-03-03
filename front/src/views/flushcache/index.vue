<template>
  <div class="departContent app-container calendar-list-container">
    <!-- form表 -->
    <div style="margin-top: 30px;" align="center">
      <el-form ref="addForm" :model="addForm" :rules="addFormRules" label-width="80px">
        <el-form-item label="选择机房" prop="room">
          <el-select v-model="addForm.room" value-key="id" multiple filterable style="width: 80%;">
            <el-option v-for="(item,index) in nodeList" :key="index" :label="item.room" :value="item.room"/>
          </el-select>
        </el-form-item>
        <el-form-item label="URL" prop="urls" >
          <el-input v-model="addForm.urls" :rows="8" type="textarea" placeholder="一行一个url" style="width: 80%;"/>
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer" align="center">
        <el-button @click="handleConcel" @click.native="submitLoading = false">取消</el-button>
        <el-button :loading="submitLoading" type="primary" @click.native="addSubmit">提交</el-button>
      </div>
    </div>
    <div style="margin-top: 50px; margin-left: 50px;">
     <div v-for="(data,url) in statusList.success" :key="url" >
          <el-button style="width: 200px;">{{url}}</el-button>
          <el-tag v-for="ip in data" type="success" :key="ip" style="margin-right:10px">
            {{ip}}
          </el-tag>
      </div>
      <div v-for="(data,url) in statusList.fail" :key="url" >
          {{url}}
          <el-tag v-for="ip in data" type="danger" :key="ip" style="margin-right:10px">
            {{ip}}
          </el-tag>
      </div>
    </div>
  </div>
</template>

<script>
import { getNodelist, postAdd } from '@/api/api'
export default {
  data() {
    return {
      info_title: '缓存刷新',
      submitLoading: false,
      nodeList: [],
      statusList: [],
      addFormRules: {
        // room: [{
        //   required: true,
        //   message: '不能为空',
        //   trigger: 'blur'
        // }],
        urls: [{
          required: true,
          message: '不能为空',
          trigger: 'blur'
        }]
      },
      addForm: {
        room: '',
        urls: ''
      }
    }
  },
  created() {
    this.get_nodelist()
  },

  methods: {
    // 取消内容
    handleConcel() {
      this.addForm.urls = ''
    },
    get_nodelist() {
      getNodelist()
        .then(res => {
          this.nodeList = res.data.data
        })
    },
    addSubmit() {
      this.$refs.addForm.validate((valid) => {
        if (valid) {
        this.$confirm('确认提交吗？', '提示', {}).then(() => {
          this.submitLoading = true
          const params = Object.assign({}, this.addForm)
          postAdd(params)
            .then((res) => {
              this.statusList = res.data
              this.submitLoading = false
              this.$message({
                message: '提交成功',
                type: 'success'
              })
            })
          })
        }
      })
    },
  }
}
</script>

<style lang="scss" scoped>
  .search {
    width: 100%;
    margin-top: 30px;
  }
</style>