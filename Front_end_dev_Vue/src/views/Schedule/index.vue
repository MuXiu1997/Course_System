<!--suppress CssUnusedSymbol, JSUnusedGlobalSymbols -->
<template>
  <div class="schedule" v-show="show">

    <!--四个图标-->
    <i class="el-icon-folder-checked i-button"
       @click="save"
       style="right: 10px;"
    >
    </i>
    <i class="el-icon-download i-button"
       @click="getXlsx"
       style="right: 60px;"
    >
    </i>
    <i class="el-icon-circle-plus-outline i-button"
       @click="dialogVisible = true"
       style="right: 110px;"
    >
    </i>
    <i class="el-icon-user i-button"
       @click="toAdmin"
       style="left: 10px;"
    >
    </i>

    <!--新建班级-->
    <el-dialog
      title="新建班级"
      :visible.sync="dialogVisible"
      width="30%"
      append-to-body
      center>
      <el-input
        placeholder="请输入班级名"
        v-model="newClassName"
        @keydown.native.enter="createNewClass"
        prefix-icon="el-icon-edit-outline">
      </el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="createNewClass">确 定</el-button>
      </span>
    </el-dialog>

    <!--左上角固定位置-->
    <div class="left-top">
      <div class="left-top-inner">
        <span style="font-size: 16px">班次</span>
      </div>
    </div>

    <!--首列-->
    <div
      id="firstColumn"
      ref="firstColumn"
    >
      <div
        v-for="(row,rowIndex) in table.rowHeader"
        :key="rowIndex"
        class="firstColumn-cell"
      >
        <div
          class="firstColumn-cell-content"
        >
          {{ row.className }}
        </div>
      </div>
      <!--延长此列，使滚动条联动不出现问题-->
      <div style="height: 200px">
      </div>
    </div>
    <!--表头-->
    <div
      id="tableHeader"
      ref="tableHeader"
    >
      <div v-for="(col,colIndex) in table.headersAndOptions"
           :key="colIndex"
           class="tableHeader-cell"
      >
        <span style="font-size: 16px">{{ col.title }}</span>
      </div>
      <!--延长此行，使滚动条联动不出现问题-->
      <div style="width: 100px;display: inline-block;">
      </div>
    </div>
    <!--table-->
    <div
      class="scrollStyle table-body"
      ref="tableMain"
      @scroll="linkScroll()"
    >
      <div
        v-for="(row,rowIndex) in table.schedulesData"
        :key="rowIndex"
        class="table-row"
      >
        <div
          v-for="(col,colIndex) in row"
          :key="`${rowIndex},${colIndex}`"
          class="table-col"
        >

          <!--单元格-->
          <ScheduleCell
            :col="col"
            :currentEdit.sync="currentEdit"
            :rowIndex="rowIndex"
            :colIndex="colIndex"
            @change="calcDate(row, colIndex)"
            @check="checkDuplicate"
            @mouseenter.native="enterCurrentDuplicate(col,`${rowIndex}-${colIndex}`)"
            :options="table.headersAndOptions[colIndex].options"
            :ref="`${rowIndex}-${colIndex}`"
          >
          </ScheduleCell>

        </div>
        <!--延长-->
        <div style="width: 20px;display: inline-block">
        </div>
      </div>
      <!--延长-->
      <div style="height: 100px">
      </div>
    </div>
  </div>

</template>

<script>
import { Notification, Loading, Dialog, Button, Input } from 'element-ui'

import ScheduleCell from './components/ScheduleCell.vue'

import { setWorkdayData, calculationDate, duplicateChecking } from './modules/dateCalc.js'

export default {
  name: 'Schedule',
  components: {
    'el-dialog': Dialog,
    'el-button': Button,
    'el-input': Input,
    ScheduleCell
  },
  data () {
    return {
      show: false,

      newClassName: '',
      dialogVisible: false,

      currentEdit: '',

      tempEnter: {
        col: null,
        ref: null
      },

      // table初始默认数据
      table: {
        headersAndOptions: [
          {
            id: 0,
            options: [],
            title: null
          }
        ],
        rowHeader: [
          {
            id: 0,
            className: ''
          }
        ],
        schedulesData: [
          [
            {
              startDate: null,
              endDate: null,
              duration: null,
              teacher: null,
              conflictArray: []
            }
          ]
        ]
      }
    }
  },
  created () {
    let loading = Loading.service(
      {
        fullscreen: true,
        text: 'Loading...',
        lock: true
      }
    )
    this.$axios.get('/api/workdays')
      .then(response => {
        setWorkdayData(response.data['isWorkdayData'])
      })
    this.$axios.get('/api/schedules', {})
      .then(response => {
        this.table = response.data
      })
    this.checkDuplicate()
    this.$nextTick(() => {
      setTimeout(() => {
        loading.close()
        this.show = true
      }, 500)
    })
  },
  methods: {
    edit (rowIndex, colIndex) {
      this.currentEdit = `${rowIndex}-${colIndex}`
    },
    toAdmin () {
      location.href = '/admin'
    },
    // 滚动条联动
    linkScroll () {
      this.$refs.tableHeader.scrollLeft = this.$refs.tableMain.scrollLeft
      this.$refs.firstColumn.scrollTop = this.$refs.tableMain.scrollTop
    },
    createNewClass () {
      this.dialogVisible = false
      this.$axios.post(`/api/schedules/${this.newClassName}`, {})
        .then(response => {
          this.table = response.data
          Notification({
            title: 'success',
            message: '班级添加成功',
            type: 'success'
          })
        })
        .catch(error => {
          console.log(error)
          Notification({
            title: 'error',
            message: '添加失败',
            type: 'error'
          })
        })
    },
    save () {
      this.$axios.post('/api/schedules', this.table)
        .then(() => {
          Notification({
            title: 'success',
            message: '保存成功',
            type: 'success'
          })
        })
        .catch(error => {
          console.log(error)
          Notification({
            title: 'error',
            message: '保存失败',
            type: 'error'
          })
        })
    },
    getXlsx () {
      this.$axios.post('/xlsx', this.table, {
        responseType: 'blob'
      })
        .then((response) => {
          let date = new Date()
          let blob = new Blob([response.data], { type: 'application/octet-stream' })
          let fileName = `百知教育课表${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日.xlsx`
          let link = document.createElement('a')
          link.style.display = 'none'
          if ('download' in document.createElement('a')) { // 非IE下载
            link.download = fileName
            link.href = window.URL.createObjectURL(blob)
            document.body.appendChild(link)
            link.click()
            URL.revokeObjectURL(link.href) // 释放URL 对象
          } else { // IE10+下载
            navigator.msSaveBlob(blob, fileName)
          }
          document.body.removeChild(link)
        })
        .catch(error => {
          console.log(error)
          Notification({
            title: 'error',
            message: '下载失败',
            type: 'error'
          })
        })
    },
    // #################################################################################################################
    // 时间推算
    calcDate (row, colIndex) {
      calculationDate(row, colIndex)
      this.checkDuplicate()
    },
    // 查重
    checkDuplicate () {
      duplicateChecking(this.table.schedulesData)
    },
    // #################################################################################################################
    enterCurrentDuplicate (col, ref) {
      if (col.conflictArray.length === 0) {
        return
      }
      if (this.tempEnter.col && this.tempEnter.ref) {
        if (this.tempEnter.col === col && this.tempEnter.ref === ref) {
          return
        } else {
          this.leaveCurrentDuplicate(this.tempEnter.col, this.tempEnter.ref)
        }
      }
      this.tempEnter.col = col
      this.tempEnter.ref = ref
      this.$refs[ref][0].$el.classList.add('current')
      for (let i = 0; i < col.conflictArray.length; i++) {
        this.$refs[col.conflictArray[i]][0].$el.classList.add('currentDuplicate')
      }
    },
    leaveCurrentDuplicate (col, ref) {
      this.$refs[ref][0].$el.classList.remove('current')
      for (let i = 0; i < col.conflictArray.length; i++) {
        this.$refs[col.conflictArray[i]][0].$el.classList.remove('currentDuplicate')
      }
    }
  }
}
</script>

<style scoped>
  .schedule {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
  }

  .left-top {
    width: 140px;
    height: 57px;
    position: fixed;
    top: 0;
    left: 0;
    padding-top: 4px;
    padding-left: 20px;
  }

  .left-top-inner {
    height: 53px;
    line-height: 50px;
    text-align: center;
    border-top: 1px solid #dee2e6;
    border-bottom: 2px solid #dee2e6;
  }

  /*背景色************************************/
  .duplicate {
    background-color: #f4f4f5;
  }

  .currentDuplicate {
    background-color: #b3d8ff;
  }

  .current.duplicate {
    background-color: #409EFF;
  }

  /********************************************/

  #tableHeader {
    position: absolute;
    top: 0;
    right: 0;
    left: 140px;
    white-space: nowrap;
    padding: 4px 20px 0 0;
    overflow: hidden;
    height: 57px;
    z-index: 100;
  }

  #tableHeader::-webkit-scrollbar {
    display: none !important;
  }

  .tableHeader-cell {
    display: inline-block;
    width: 304px;
    height: 53px;
    line-height: 50px;
    text-align: center;
    border-top: 1px solid #dee2e6;
    border-bottom: 2px solid #dee2e6;
  }

  #firstColumn {
    position: absolute;
    top: 57px;
    bottom: 0;
    left: 0;
    overflow: hidden;
  }

  #firstColumn::-webkit-scrollbar {
    display: none !important;
  }

  .firstColumn-cell {
    width: 140px;
    height: 204px;
    padding-left: 20px;
    background-color: white;
    z-index: 100000
  }

  .firstColumn-cell-content {
    text-align: center;
    line-height: 200px;
    height: 203px;
    border-bottom: 1px solid #dee2e6;
    border-right: 1px solid #dee2e6;
    background-color: white;
    z-index: 100000
  }

  .table-body {
    position: absolute;
    top: 56px;
    right: 0;
    bottom: 0;
    left: 140px;
    overflow: auto
  }

  .table-row {
    white-space: nowrap;
  }

  .table-col {
    display: inline-block;
    padding: 2px;
    width: 304px;
    height: 204px;
    border-bottom: 1px solid #dee2e6;
  }

  .i-button {
    position: fixed;
    padding: 5px;
    bottom: 10px;
    font-size: 30px;
    background-color: #fff;
    color: rgba(45, 140, 240, 0.2);
    border-radius: 20%;
    border: 2px rgba(45, 140, 240, 0.2) solid;
    z-index: 10000;
  }

  .i-button:hover {
    color: rgba(45, 140, 240, 1) !important;
    border: 2px rgba(45, 140, 240, 1) solid !important;
  }

</style>
