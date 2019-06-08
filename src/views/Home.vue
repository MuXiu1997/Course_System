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
       @click="save(false)"
       style="right: 10px;"
    >
    </i>
    <i class="el-icon-download"
       @click="save(true)"
       style="right: 60px;"
    >
    </i>
    <i class="el-icon-circle-plus-outline"
       @click="modalKey = true"
       style="right: 110px;"
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
           overflow: auto;"
         id="firstColumn"
         ref="firstColumn"
    >
      <div v-for="(row,rowIndex) in tableData" :key="''+row+rowIndex"
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
          {{ row[columnsData.length] }}
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
           overflow: auto;
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
         class="scrollStyle"
         ref="tableMain"
         @scroll="linkScroll()"
    >
      <div v-for="(row,rowIndex) in tableData" :key="''+row+rowIndex"
           style="white-space:nowrap;">
        <div v-for="(col,colIndex) in columnsData" :key="''+col+colIndex"
             style="display: inline-block;padding: 2px;width: 304px;height: 204px;border-bottom: 1px solid #dee2e6;">
          <div style="padding: 20px 18px;border-radius: 2.5%;"
               :class="{
                 'duplicate':isDuplicate(rowIndex,colIndex),
                 'currentDuplicate':isCurrentDuplicate(rowIndex,colIndex),
                 'current':isCurrent(rowIndex,colIndex) && isDuplicate(rowIndex,colIndex),
                 'date':true
               }"
               @mouseover="mouseover(rowIndex,colIndex)"
          >
            <div>
              开始日期：
              <DatePicker
                type="date"
                placeholder="Select date"
                v-model="tableData[rowIndex][colIndex].startDate"
                format="yyyy年M月d日"
                :clearable="false"
                style="width: 200px"
                @on-change="calculationEndDate(tableData[rowIndex],colIndex)"
              >
              </DatePicker>
            </div>
            <div>
              结束日期：
              <DatePicker
                type="date"
                placeholder="Select date"
                format="yyyy年M月d日"
                disabled
                v-model="tableData[rowIndex][colIndex].endDate"
                style="width: 200px">
              </DatePicker>
            </div>
            <div>
              周&emsp;&emsp;期：
              <el-input-number
                size="mini"
                v-model="tableData[rowIndex][colIndex].duration"
                :min="0"
                @change="calculationEndDate(tableData[rowIndex],colIndex)"
              >
              </el-input-number>
            </div>
            <div>
              <label>
                讲&emsp;&emsp;师：
                <Select v-model="tableData[rowIndex][colIndex].teacher" style="width:200px"
                        @on-change="duplicateChecking()">
                  <Option v-for="options in optionsData[colIndex]" :value="options" :key="options">{{ options }}
                  </Option>
                </Select>
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
</template>

<script>
import { Notification } from 'element-ui'

export default {
  name: 'home',
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
      columnsData: [],
      optionsData: [],
      tableData: [
        { teacher: null }
      ],
      isWorkdayData: {}
    }
  },
  created () {
    this.load()
    let date = new Date()
    this.$axios.get('/api/GET/workday-data', {
      params: {
        year: date.getFullYear()
      }
    })
      .then(response => {
        this.isWorkdayData = response.data['isWorkdayData']
      })
  },
  mounted () {
    this.$nextTick(() => {
      setTimeout(() => {
        this.loading = false
      }, 500)
    })
  },
  methods: {
    createNewClass () {
      this.$axios.post('/api/POST/new-class', {
        'newClassName': this.newClassName
      })
        .then(response => {
          this.tableData.push(response.data['newClass'])
        })
    },
    linkScroll () {
      this.$refs.tableHead.scrollLeft = this.$refs.tableMain.scrollLeft
      this.$refs.firstColumn.scrollTop = this.$refs.tableMain.scrollTop
    },
    save (isXlsx) {
      this.$axios.post('/api/POST/table-data', {
        'tableData': this.tableData,
        'isXlsx': isXlsx
      })
        .then(response => {
          console.log(response.status)
          if (isXlsx) {
            if (response.status === 200) {
              location.href = '/xlsx/' + response.data['fileName']
            } else {
              Notification({
                title: 'error',
                message: '获取文件失败',
                type: 'error'
              })
            }
          } else {
            if (response.status === 200) {
              Notification({
                title: 'success',
                message: '保存成功',
                type: 'success'
              })
            } else {
              Notification({
                title: 'error',
                message: '保存失败',
                type: 'error'
              })
            }
          }
        })
        .catch(error => {
          console.log(error)
        })
    },
    // load (_time) {
    load () {
      this.$axios.get('/api/GET/table-data', {
        // params: {
        //   time: _time
        // }
      })
        .then(response => {
          this.tableData = response.data['tableData']
          this.columnsData = response.data['columnsData']
          this.optionsData = response.data['optionsData']
        })
    },
    // #################################################################################################################
    // 时间推算
    getNextWorkDay (startDate, duration) {
      let dateObj = new Date(startDate)
      while (duration !== 0) {
        // console.log(1111111)
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
    calculationEndDate (rowArray, colIndex) {
      let thisObj = rowArray[colIndex]
      if (thisObj.startDate && thisObj.duration) {
        thisObj.endDate = this.getNextWorkDay(thisObj.startDate, thisObj.duration - 1)
      } else {
        thisObj.endDate = null
      }

      if (thisObj.startDate && ++colIndex < this.columnsData.length) {
        let nextObj = rowArray[colIndex]
        nextObj.startDate = this.getNextWorkDay(thisObj.startDate, thisObj.duration)
        this.calculationEndDate(rowArray, colIndex)
      } else {
        // console.log(765566)
        this.duplicateChecking()
      }
    },
    // #################################################################################################################
    // 重复单元格增加class
    isDuplicate (rowIndex, colIndex) {
      return this.tableData[rowIndex][colIndex].conflictArray.length > 0
    },
    isCurrentDuplicate (rowIndex, colIndex) {
      return this.tableData[rowIndex][colIndex].conflictArray
        .filter(conflict => conflict === this.currentStr)
        .length > 0
    },
    mouseover (rowIndex, colIndex) {
      this.currentStr = '' + rowIndex + ',' + colIndex
      this.current = [rowIndex, colIndex]
    },
    isCurrent (rowIndex, colIndex) {
      return rowIndex === this.current[0] && colIndex === this.current[1]
    },
    // #################################################################################################################
    duplicateChecking () {
      for (let i = 0; i < this.tableData.length; i++) {
        for (let j = 0; j < this.columnsData.length; j++) {
          this.tableData[i][j].conflictArray = []
        }
      }
      for (let i = 0; i < this.tableData.length; i++) {
        for (let j = 0; j < this.columnsData.length; j++) {
          for (let x = i + 1; x < this.tableData.length; x++) {
            for (let y = 0; y < this.columnsData.length; y++) {
              let obj1 = this.tableData[i][j]
              let obj2 = this.tableData[x][y]

              if (obj1.endDate && obj2.endDate && obj1.teacher && obj2.teacher) {
                // console.log(obj1.startDate.valueOf(), obj2.startDate.valueOf())
                if (obj1.teacher === obj2.teacher) {
                  if (obj2.startDate.valueOf() <= obj1.endDate.valueOf()) { // 逻辑仍需补充
                    obj1.conflictArray.push('' + x + ',' + y)
                    obj2.conflictArray.push('' + i + ',' + j)
                    // console.log(obj1, obj2)
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
