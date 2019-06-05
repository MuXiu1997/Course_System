<template>
  <div class="home" style="position: fixed;top: 0;right: 0;bottom: 0;left: 0">
     <Drawer title="Basic Drawer" :closable="false" v-model="value1" transfer>
        <p>Some contents...</p>
        <p>Some contents...</p>
        <p>Some contents...</p>
    </Drawer>
    <div style=
           "position: absolute;
           top: 0;
           right: 0;
           left: 0;
           white-space:nowrap;
           padding: 4px 20px 0 20px;
           overflow: auto;
           height: 57px;"
         id="aaaaaaa"
         ref="aaaaaaa"
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
    </div>
    <div style="position: absolute;top: 56px;right: 0;bottom: 0;left: 0;padding: 0 20px;overflow: auto"
         class="scrollStyle"
         ref="bbbbbbbb"
         @scroll="sssss()"
    >
      <div v-for="(v,rowIndex) in tableData" :key="''+v+rowIndex"
           style="white-space:nowrap;">
        <div v-for="(v,colIndex) in columnsData" :key="''+v+colIndex"
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
            <i class="el-icon-edit-outline"
               @click="save()"
               style=
                 "position: fixed;
             padding: 5px;
             right: -5px;
             top: 257px;
             transform:translateY(-50%);
             font-size: 30px;
             background-color: #fff;
             color: rgba(45, 140, 240, 0.1);
             border-radius: 20%;
             border: 2px rgba(45, 140, 240, 0.1) solid;
             z-index: 10000;"
            ></i>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'home',
  data () {
    return {
      value1: false,
      currentStr: '',
      current: [],
      clientHeight: '',
      clientWidth: '',
      columnsData: [],
      optionsData: [],
      tableData: [
        // [
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 20,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 6,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 4,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 20,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 10,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 15,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 15,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 20,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   'Python161'
        // ],
        // [
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 20,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 6,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 4,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 20,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 10,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 15,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 15,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 20,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   'Python165'
        // ],
        // [
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 20,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 6,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 4,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 20,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 10,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 15,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 15,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 20,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   'Python165'
        // ],
        // [
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 20,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 6,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 4,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 20,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 10,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 15,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 15,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 20,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   'Python165'
        // ],
        // [
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 20,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 6,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 4,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 20,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 10,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 15,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 15,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   {
        //     startDate: null,
        //     endDate: null,
        //     duration: 20,
        //     teacher: null,
        //     conflictArray: []
        //   },
        //   'Python165'
        // ]
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
  // mounted () {
  //   // 获取浏览器可视区域高度宽度
  //   this.clientHeight = `${document.documentElement.clientHeight}` - 1// document.body.clientWidth;
  //   this.clientWidth = `${document.documentElement.clientWidth}` - 1
  //   // console.log(this.clientWidth)
  //   let _this = this
  //   window.onresize = function temp () {
  //     _this.clientHeight = `${document.documentElement.clientHeight}` - 1
  //     _this.clientWidth = `${document.documentElement.clientWidth}` - 1
  //     // console.log(this.clientWidth)
  //   }
  //   this.$nextTick(() => {
  //     this.duplicateChecking()
  //   })
  // },
  methods: {
    sssss () {
      this.$refs.aaaaaaa.scrollLeft = this.$refs.bbbbbbbb.scrollLeft / this.$refs.bbbbbbbb.scrollWidth * this.$refs.aaaaaaa.scrollWidth
    },
    save () {
      this.$axios.post('/api/POST/table-data', {
        'tableData': this.tableData
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
        console.log(765566)
        // this.duplicateChecking()
      }
    },
    // #################################################################################################################
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
      // console.log(123)
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
