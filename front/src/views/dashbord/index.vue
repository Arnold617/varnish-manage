<template>
  <div class="udcDashbord">
    <div class="filter-container">
      <el-radio-group v-model="query.status" size="small" class="filter-item" @change="getData">
        <el-radio-button :label="null">全部</el-radio-button>
        <el-radio-button v-for="(val,key) in statusMsg" :label="key" :key="key">{{ val }}</el-radio-button>
      </el-radio-group>
      <!-- <el-button size="small" class="filter-item" @click="getData" /> -->
    </div>
    <el-row v-loading="listLoading" :gutter="10" style="margin-top:20px">

      <el-col v-for=" item in dataList" :span="6" :key="item.id" style="margin-top:3px">
        <div :class="{'updateBox':item.status==0,'nodeBox':item.status==1,'errBox':item.status==2}">
          <div class="title">
            <el-tag :type="statusTypes[item.status]">{{ statusMsg[item.status] }}</el-tag>
          </div>
          <table class="tableClass">
            <tr>
              <td class="name">IP</td>
              <td class="content">{{ item.ip }}</td>
            </tr>
            <tr>
              <td class="name">机房</td>
              <td class="content">
                {{ item.room.idc }}
              </td>
            </tr>
            <tr>
              <td class="name">update</td>
              <td class="content">
                {{ item.updated_at }}
              </td>
            </tr>
            <!--            <tr v-show="item.status==2">
              <td class="name">失败信息</td>
              <td class="content">
                {{ item.err_msg }}
              </td>
            </tr> -->
          </table>

        </div>

      </el-col>
    </el-row>
  </div>
</template>
<script>
import { getVarnishList } from '@/api/api'
export default {
  data() {
    return {
      dataList: [],
      query: {
        // limit: 999,
        status: null
      },
      listLoading: true,
      statusTypes: ['', 'warning', 'danger'],
      statusMsg: ['更新成功', '等待更新', '更新失败']
    }
  },

  created() {
    this.getData()
  },
  methods: {
    // 获取列表数据
    getData() {
      this.listLoading = true
      getVarnishList(this.query).then(
    //   getList('/api/proxy/uvarnish/varnishList/', this.query).then(
        response => {
          this.listLoading = false
          this.dataList = response.data.data
          // console.log(response.data.data)
        },
        error => {
          this.listLoading = false
        }
      )
    }
  }
}
</script>
<style lang="scss" scoped>
  .udcDashbord {
    margin: 20px;
    color: #373d41;
    font-size: 14px;
    line-height: 0.2;

    .nodeBox {
      height: 150px;
      background-color: #ffffff;
      border: 1px dashed #ff7800;
      padding: 10px;

      .title {
        width: 100%;
        height: 35px;
        text-align: center;
        font-weight: 600;
      }

      .tableClass {
        width: 100%;
        height: 110px;

        tr {
          .name {
            font-weight: 600;
            width: 20%;
            text-align: right;
          }

          .content {
            padding: 0 40px;
            overflow: hidden;
            text-align: center;
          }
        }
      }
    }

    .updateBox {
      height: 150px;
      background-color: #fbfbfb;
      border: 1px dotted #409eff;
      padding: 10px;

      .title {
        width: 100%;
        height: 35px;
        text-align: center;
        font-weight: 600;
      }

      .tableClass {
        width: 100%;
        height: 110px;

        tr {
          .name {
            font-weight: 600;
            width: 20%;
            text-align: right;
          }

          .content {
            padding: 0 40px;
            overflow: hidden;
            text-align: center;
          }
        }
      }
    }

    .errBox {
      height: 150px;
      background-color: #fbfbfb;
      border: 1px dotted red;
      padding: 10px;

      .title {
        width: 100%;
        height: 30px;
        text-align: center;
        font-weight: 600;
      }

      .tableClass {
        width: 100%;
        height: 110px;

        tr {
          .name {
            font-weight: 600;
            width: 20%;
            text-align: right;
          }

          .content {
            padding: 0 40px;
            overflow: hidden;
            text-align: center;
          }
        }
      }
    }
  }
</style>
