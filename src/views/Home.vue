<template>
  <div class="home"
  >
    <Table
      :height="clientHeight"
      :width="clientWidth"
      :columns="columnsData"
      :data="tableData"
      ref="courseTable"
      class="scrollStyle"
    >
      <template v-for="(col,colIndex) in columnsData" slot-scope="{ row, index }" :slot="col.slot">
        <div style="padding: 20px 18px;border-radius: 2.5%;" :key="''+index+colIndex"
             :class="{
             'duplicate': isDuplicate(index,colIndex),
             'currentDuplicate':isCurrentDuplicate(index,colIndex),
             'current':isCurrent(index,colIndex) &&isDuplicate(index,colIndex),
             'date':true
             }"
             @mouseover="mouseover(index,colIndex)"
        >
          <div>
            开始日期：
            <DatePicker
              type="date"
              placeholder="Select date"
              v-model="row[col.slot].startDate"
              format="yyyy年M月d日"
              :clearable="false"
              style="width: 200px"
              @on-change="calculationEndDate(row,colIndex)"
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
              v-model="row[col.slot].endDate"
              style="width: 200px">

            </DatePicker>
          </div>
          <div>
            周&emsp;&emsp;期：
            <el-input-number
              size="mini"
              v-model="row[col.slot].duration"
              :min="0"
              @change="calculationEndDate(row,colIndex)"
            >
            </el-input-number>
          </div>
          <div>
            <label>
              讲&emsp;&emsp;师：
              <Select v-model="row[col.slot].teacher" style="width:200px" @on-change="duplicateChecking()">
                <Option v-for="options in optionsData[colIndex-1]" :value="options" :key="options">{{ options }}
                </Option>
              </Select>
            </label>
          </div>
          <i class="el-icon-edit-outline"
             @click="save()"
             style=
               "position: fixed;
             padding: 5px;
             right: -5px;
             top: 50%;
             transform:translateY(-50%);
             font-size: 30px;
             color: rgba(45, 140, 240, 0.1);
             border-radius: 20%;
             border: 2px rgba(45, 140, 240, 0.1) solid;"
          ></i>
        </div>
      </template>
    </Table>
  </div>
</template>

<script>
export default {
  name: 'home',
  data () {
    return {
      currentStr: '',
      current: [],
      clientHeight: '',
      clientWidth: '',
      columnsData: [],
      optionsData: [],
      tableData: [
        {
          0: 'Python161',
          1: {
            startDate: null,
            endDate: null,
            duration: 0,
            teacher: null,
            conflictArray: []
          }
        }
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
    this.$axios.get('/api/GET/columns-data')
      .then(response => {
        this.columnsData = response.data['columnsData']
      })
    this.$axios.get('/api/GET/options-data')
      .then(response => {
        this.optionsData = response.data['optionsData']
      })
  },
  mounted () {
    // 获取浏览器可视区域高度宽度
    this.clientHeight = `${document.documentElement.clientHeight}` - 1// document.body.clientWidth;
    this.clientWidth = `${document.documentElement.clientWidth}` - 1
    // console.log(this.clientWidth)
    let _this = this
    window.onresize = function temp () {
      _this.clientHeight = `${document.documentElement.clientHeight}` - 1
      _this.clientWidth = `${document.documentElement.clientWidth}` - 1
      // console.log(this.clientWidth)
    }
    this.$nextTick(() => {
      this.duplicateChecking()
    })
  },
  methods: {
    save () {
      this.$axios.post('/api/POST/table-data', {
        'tableData': this.$refs.courseTable.$refs.tbody.$props.data
      })
    },
    load (_time) {
      this.$axios.get('/api/GET/table-data', {
        params: {
          time: _time
        }
      })
        .then(response => {
          this.tableData = response.data['tableData']
        })
    },
    // #################################################################################################################
    // 时间推算
    getNextWorkDay (startDate, duration) {
      let dateObj = new Date(startDate)
      while (duration !== 0) {
        console.log(1111111)
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
    calculationEndDate (rowObj, colIndex) {
      let thisObj = rowObj[Object.keys(rowObj)[colIndex]]
      if (thisObj.startDate && thisObj.duration) {
        thisObj.endDate = this.getNextWorkDay(thisObj.startDate, thisObj.duration - 1)
      } else {
        thisObj.endDate = null
      }

      if (thisObj.startDate && ++colIndex < this.columnsData.length) {
        let nextObj = rowObj[Object.keys(rowObj)[colIndex]]
        nextObj.startDate = this.getNextWorkDay(thisObj.startDate, thisObj.duration)
        this.calculationEndDate(rowObj, colIndex)
      } else {
        console.log(765566)
        this.duplicateChecking()
      }
    },
    // #################################################################################################################
    isDuplicate (rowIndex, colIndex) {
      if (this.$refs.courseTable) {
        let tableData = this.$refs.courseTable.$refs.tbody.$props.data
        return tableData[rowIndex][Object.keys(tableData[rowIndex])[colIndex]].conflictArray.length > 0
      } else {
        return false
      }
    },
    isCurrentDuplicate (rowIndex, colIndex) {
      if (this.$refs.courseTable) {
        let tableData = this.$refs.courseTable.$refs.tbody.$props.data
        return tableData[rowIndex][Object.keys(tableData[rowIndex])[colIndex]].conflictArray
          .filter(conflict => conflict === this.currentStr)
          .length > 0
      } else {
        return false
      }
    },
    mouseover (rowIndex, colIndex) {
      this.currentStr = '' + rowIndex + ',' + colIndex
      this.current = [rowIndex, colIndex]
    },
    isCurrent (rowIndex, colIndex) {
      return rowIndex === this.current[0] && colIndex === this.current[1]
    },
    duplicateChecking () {
      let tableData = this.$refs.courseTable.$refs.tbody.$props.data
      // console.log(123)
      for (let i = 0; i < this.tableData.length; i++) {
        for (let j = 1; j < this.columnsData.length; j++) {
          tableData[i][Object.keys(tableData[i])[j]].conflictArray = []
        }
      }
      for (let i = 0; i < this.tableData.length; i++) {
        for (let j = 0; j < this.columnsData.length; j++) {
          for (let x = i + 1; x < this.tableData.length; x++) {
            for (let y = 0; y < this.columnsData.length; y++) {
              let obj1 = tableData[i][Object.keys(tableData[i])[j]]
              let obj2 = tableData[x][Object.keys(tableData[x])[y]]

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
