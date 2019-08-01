<template>
  <div class="home" style="position: fixed;top: 0;right: 0;bottom: 0;left: 0">

    <!--加载界面-->
    <Spin fix v-if="loading">
      <i class="el-icon-loading"
         style=
           "font-size: 30px;
           background-color: #fff;
           color: rgba(45, 140, 240, 0.8);
           z-index: 999999;"
      >
      </i>
      <div style="color: rgba(45, 140, 240, 0.8);font-size: 16px">Loading...</div>
    </Spin>

    <!--三个图标-->
    <i class="el-icon-folder-checked"
       @click="save"
       style="right: 10px;"
    >
    </i>
    <i class="el-icon-download"
       @click="getXlsx"
       style="right: 60px;"
    >
    </i>
    <i class="el-icon-circle-plus-outline"
       @click="modalKey = true"
       style="right: 110px;"
    >
    </i>
    <i class="el-icon-user"
       @click="toAdmin"
       style="left: 10px;"
    >
    </i>
    <!--    <Drawer title="Basic Drawer" :closable="false" v-model="value1" transfer>-->
    <!--      <p>Some contents...</p>-->
    <!--      <p>Some contents...</p>-->
    <!--      <p>Some contents...</p>-->
    <!--    </Drawer>-->

    <!--新建班级对话框-->
    <Modal
      v-model="modalKey"
      title="新建班级"
      @on-ok="createNewClass()"
      @on-cancel="modalKey = false"
      style="text-align: center"
    >
      <label>班级名：<Input v-model="newClassName" placeholder="请输入班级名" clearable style="width: 200px"/></label>
    </Modal>

    <!--左上角固定位置-->
    <div style="width: 140px;height: 57px;position: fixed;top: 0;left: 0;padding-top: 4px;padding-left: 20px">
      <div style="height: 53px;
             line-height: 50px;
             text-align: center;
             border-top: 1px solid #dee2e6;
             border-bottom: 2px solid #dee2e6;">
        <span style="font-size: 16px">班次</span>
      </div>
    </div>

    <!--列首-->
    <div style=
           "position: absolute;
           top: 57px;
           bottom: 0;
           left: 0;
           overflow: hidden;"
         id="firstColumn"
         ref="firstColumn"
    >
      <div v-for="(row,rowIndex) in schedulesData" :key="''+row+rowIndex"
           style="width: 140px;height: 204px;padding-left: 20px;background-color: white;z-index: 100000"
      >
        <div style="
             text-align: center;
             line-height: 200px;
             height: 203px;
             border-bottom: 1px solid #dee2e6;
             border-right: 1px solid #dee2e6;
             background-color: white;
             z-index: 100000"
        >
          {{ row.className }}
        </div>
      </div>
      <div style="height: 200px">
      </div>
    </div>
    <!--表头-->
    <div style=
           "position: absolute;
           top: 0;
           right: 0;
           left: 140px;
           white-space:nowrap;
           padding: 4px 20px 0 0;
           overflow: hidden;
           height: 57px;
           z-index: 100;"
         id="tableHead"
         ref="tableHead"
    >
      <div v-for="col in columnsData"
           :key="col.title"
           style=
             "display: inline-block;
             width: 304px;
             height: 53px;
             line-height: 50px;
             text-align: center;
             border-top: 1px solid #dee2e6;
             border-bottom: 2px solid #dee2e6;"
      >
        <span style="font-size: 16px">{{ col.title }}</span>
      </div>
      <div style="width: 100px;display: inline-block;">

      </div>
    </div>
    <!--table-->
    <div style="position: absolute;top: 56px;right: 0;bottom: 0;left: 140px;overflow: auto"
         class="scrollStyle clusterize-scroll"
         id="scrollArea"
         ref="tableMain"
         @scroll="linkScroll()"
    >
      <div id="contentArea" class="clusterize-content">
        <div v-for="(row,rowIndex) in schedulesData" :key="''+rowIndex"
             style="white-space:nowrap;">
          <div v-for="(col,colIndex) in row.majorInfos" :key="''+rowIndex+colIndex"
               style="display: inline-block;padding: 2px;width: 304px;height: 204px;border-bottom: 1px solid #dee2e6;">
            <div style="padding: 20px 18px;border-radius: 2.5%;"
                 class="date"
                 :class="{
                 'duplicate':isDuplicate(col),
                 'currentDuplicate':isCurrentDuplicate(col),
                 'current':isCurrent(rowIndex,colIndex)
               }"
                 @mouseenter="currentClick(rowIndex,colIndex,col)"
            >
              <div>
                开始日期：
                <DatePicker
                  type="date"
                  placeholder="Select date"
                  v-model="col.startDate"
                  format="yyyy年M月d日"
                  :clearable="false"
                  style="width: 200px"
                  @on-change="calculationEndDate(row,colIndex)"
                  transfer
                >
                </DatePicker>
              </div>
              <div>
                结束日期：
                <DatePicker
                  type="date"
                  format="yyyy年M月d日"
                  disabled
                  v-model="col.endDate"
                  style="width: 200px">
                </DatePicker>
              </div>
              <div>
                周&emsp;&emsp;期：
                <el-input-number
                  size="mini"
                  v-model="col.duration"
                  :min="0"
                  @change="calculationEndDate(row,colIndex)"
                >
                </el-input-number>
              </div>
              <div>
                <label>
                  讲&emsp;&emsp;师：
                  <el-select v-model="col.teacher"
                             clearable
                             popper-append-to-body
                             placeholder="请选择" size="mini"
                             @change="duplicateChecking()"
                  >
                    <el-option
                      v-for="option in columnsData[colIndex].options"
                      :key="option"
                      :label="option"
                      :value="option"
                    >
                    </el-option>
                  </el-select>
                </label>
              </div>
            </div>
          </div>
          <div style="width: 20px;display: inline-block">
          </div>
        </div>
        <div style="height: 100px">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Notification, InputNumber, Select, Option } from 'element-ui'
import {
  DatePicker,
  Modal,
  Input,
  Spin
} from 'iview'

// noinspection JSUnusedGlobalSymbols
export default {
  name: 'home',
  components: {
    'DatePicker': DatePicker,
    'Modal': Modal,
    'Input': Input,
    'Spin': Spin,
    'el-input-number': InputNumber,
    'el-select': Select,
    'el-option': Option

  },
  data () {
    return {
      loading: true,
      newClassName: '',
      modalKey: false,
      value1: false,
      currentStr: '',
      current: [],
      clientHeight: '',
      clientWidth: '',
      columnsData: [
        {
          options: [],
          title: null
        }
      ],
      schedulesData: [
        {
          classID: null,
          className: null,
          majorInfos: [
            {
              startDate: null,
              endDate: null,
              duration: null,
              teacher: null,
              conflictArray: [],
              id: null
            }
          ]
        }
      ],
      isWorkdayData: {},
      mouseoverTimer: null
    }
  },
  created () {
    this.$axios.get('/api/workdays')
      .then(response => {
        this.isWorkdayData = response.data['isWorkdayData']
      })
    this.$axios.get('/api/schedules', {})
      .then(response => {
        this.schedulesData = response.data['schedulesData']
        this.columnsData = response.data['columnsData']
      })
    this.$nextTick(() => {
      setTimeout(() => {
        this.loading = false
      }, 500)
    })
  },
  methods: {
    toAdmin () {
      location.href = '/admin'
    },
    createNewClass () {
      this.$axios.post(`/api/schedules/${this.newClassName}`, {})
        .then(response => {
          this.schedulesData.push(response.data['newClass'])
        })
    },
    linkScroll () {
      this.$refs.tableHead.scrollLeft = this.$refs.tableMain.scrollLeft
      this.$refs.firstColumn.scrollTop = this.$refs.tableMain.scrollTop
    },
    save () {
      this.$axios.post('/api/schedules', {
        'schedulesData': this.schedulesData
      })
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
      this.$axios.post('/xlsx', {
        'schedulesData': this.schedulesData
      }, {
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
    calculationEndDate (row, colIndex) {
      let majorInfos = row.majorInfos
      let thisObj = majorInfos[colIndex]
      while (thisObj.startDate && colIndex < majorInfos.length) {
        if (thisObj.duration) {
          thisObj.endDate = this.getNextWorkDay(thisObj.startDate, thisObj.duration - 1)
        } else {
          thisObj.endDate = null
        }
        colIndex++
        if (colIndex < majorInfos.length) {
          let nextObj = majorInfos[colIndex]
          nextObj.startDate = this.getNextWorkDay(thisObj.startDate, thisObj.duration)
          thisObj = nextObj
        }
      }
      this.duplicateChecking()
    },
    getNextWorkDay (startDate, duration) {
      let dateObj = new Date(startDate)
      while (duration !== 0) {
        dateObj.setDate(dateObj.getDate() + 1)
        let dateStr = dateObj.getFullYear() + '-' +
            ('0' + (dateObj.getMonth() + 1)).slice(-2) + '-' +
            ('0' + dateObj.getDate()).slice(-2)
        if (this.isWorkdayData[dateStr]) {
          duration--
        }
      }
      return dateObj
    },
    // #################################################################################################################
    // 重复单元格增加class
    isDuplicate (col) {
      return col.conflictArray.length > 0
    },
    isCurrentDuplicate (col) {
      return col.conflictArray
        .filter(conflict => conflict === this.current.join(','))
        .length > 0
    },
    isCurrent (rowIndex, colIndex) {
      return [rowIndex, colIndex].toString() === this.current.toString()
    },
    currentClick (rowIndex, colIndex, col) {
      if (col.conflictArray.length > 0) {
        this.current = [rowIndex, colIndex]
      }
    },
    // #################################################################################################################
    duplicateChecking () {
      for (let i = 0; i < this.schedulesData.length; i++) {
        for (let j = 0; j < this.columnsData.length; j++) {
          this.schedulesData[i].majorInfos[j].conflictArray = []
        }
      }
      for (let i = 0; i < this.schedulesData.length; i++) {
        for (let j = 0; j < this.columnsData.length; j++) {
          for (let x = i + 1; x < this.schedulesData.length; x++) {
            for (let y = 0; y < this.columnsData.length; y++) {
              let obj1 = this.schedulesData[i].majorInfos[j]
              let obj2 = this.schedulesData[x].majorInfos[y]

              if (obj1.endDate && obj2.endDate && obj1.teacher && obj2.teacher) {
                if (obj1.teacher === obj2.teacher) {
                  if (obj1.startDate.valueOf() <= obj2.endDate.valueOf() &&
                      obj1.endDate.valueOf() >= obj2.startDate.valueOf()) {
                    obj1.conflictArray.push('' + x + ',' + y)
                    obj2.conflictArray.push('' + i + ',' + j)
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
</script>

<style scoped>
  @import "../assets/css/home.css";
</style>
