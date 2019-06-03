<template>
  <div class="home"
  >
    <Table
      :height="clientHeight"
      :width="clientWidth"
      :columns="columnsData"
      :data="tableData"
      ref="table123"
      class="scrollStyle"
    >
      <template v-for="(col,colIndex) in columnsData" slot-scope="{ row, index }" :slot="col.slot">
        <div style="padding: 20px 18px;border-radius: 2.5%;" :key="''+index+colIndex"
             :class="{'ccc': isaaaa(index,colIndex), 'date':true,'abb':isasd(index,colIndex),'qwe':isqwe(index,colIndex) &&isaaaa(index,colIndex)}"
             @mouseover="bbb(index,colIndex)"
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
              v-model="row[col.slot].cycle"
              :min="0"
              @change="calculationEndDate(row,colIndex)"
            >
            </el-input-number>
          </div>
          <div>
            <label>
              讲&emsp;&emsp;师：
              <Select v-model="row[col.slot].teacher" style="width:200px" @on-change="aaa()">
                <Option v-for="options in row[col.slot].options" :value="options" :key="options">{{ options }}
                </Option>
              </Select>
            </label>
          </div>

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
        asd: '',
        qwer: [],
        clientHeight: '',
        clientWidth: '',
        columnsData: [
          {
            title: '班级',
            key: 'className',
            width: 120,
            fixed: 'left',
            align: 'center'
          },
          {
            title: 'Python基础',
            width: 310,
            slot: 'python'
          },
          {
            title: 'Web前端',
            width: 310,
            slot: 'webFe'
          },
          {
            title: 'MySQL',
            width: 310,
            slot: 'mysql'
          },
          {
            title: 'Web后端',
            width: 310,
            slot: 'webBe'
          },
          {
            title: '中期项目',
            width: 310,
            slot: 'projectM'
          },
          {
            title: '爬虫',
            width: 310,
            slot: 'crawler'
          },
          {
            title: '后期项目',
            width: 310,
            slot: 'projectL'
          },
          {
            title: 'AI训练营',
            width: 310,
            slot: 'ai'
          }
        ],
        tableData: [
          {
            className: 'Python161',
            python: {
              startDate: null,
              endDate: null,
              cycle: 0,
              teacher: null,
              options: ['张三', '李四', '王五'],
              aaaa: []
            },
            webFe: {
              startDate: null,
              endDate: null,
              cycle: 0,
              teacher: null,
              options: ['张三', '李四', '王五'],
              aaaa: []
            },
            mysql: {
              startDate: null,
              endDate: null,
              cycle: 0,
              teacher: null,
              options: ['张三', '李四', '王五'],
              aaaa: []
            },
            webBe: {
              startDate: null,
              endDate: null,
              cycle: 0,
              teacher: null,
              options: ['张三', '李四', '王五'],
              aaaa: []
            },
            projectM: {
              startDate: null,
              endDate: null,
              cycle: 0,
              teacher: null,
              options: ['张三', '李四', '王五'],
              aaaa: []
            },
            crawler: {
              startDate: null,
              endDate: null,
              cycle: 0,
              teacher: null,
              options: ['张三', '李四', '王五'],
              aaaa: []
            },
            projectL: {
              startDate: null,
              endDate: null,
              cycle: 0,
              teacher: null,
              options: ['张三', '李四', '王五'],
              aaaa: []
            },
            ai: {
              startDate: null,
              endDate: null,
              cycle: 0,
              teacher: null,
              options: ['张三', '李四', '王五'],
              aaaa: []
            }
          },
          {
            className: 'Python162',
            python: {
              startDate: null,
              endDate: null,
              cycle: 0,
              teacher: null,
              options: ['张三', '李四', '王五'],
              aaaa: []
            },
            webFe: {
              startDate: null,
              endDate: null,
              cycle: 0,
              teacher: null,
              options: ['张三', '李四', '王五'],
              aaaa: []
            },
            mysql: {
              startDate: null,
              endDate: null,
              cycle: 0,
              teacher: null,
              options: ['张三', '李四', '王五'],
              aaaa: []
            },
            webBe: {
              startDate: null,
              endDate: null,
              cycle: 0,
              teacher: null,
              options: ['张三', '李四', '王五'],
              aaaa: []
            },
            projectM: {
              startDate: null,
              endDate: null,
              cycle: 0,
              teacher: null,
              options: ['张三', '李四', '王五'],
              aaaa: []
            },
            crawler: {
              startDate: null,
              endDate: null,
              cycle: 0,
              teacher: null,
              options: ['张三', '李四', '王五'],
              aaaa: []
            },
            projectL: {
              startDate: null,
              endDate: null,
              cycle: 0,
              teacher: null,
              options: ['张三', '李四', '王五'],
              aaaa: []
            },
            ai: {
              startDate: null,
              endDate: null,
              cycle: 0,
              teacher: null,
              options: ['张三', '李四', '王五'],
              aaaa: []
            }
          }
        ],
        isWorkdayData: {
          '2019-07-15': '工作日',
          '2019-07-09': '工作日',
          '2019-09-11': '工作日',
          '2019-02-03': '工作日',
          '2019-11-19': '工作日',
          '2019-02-25': '工作日',
          '2019-08-18': '休息日',
          '2019-03-03': '休息日',
          '2019-10-13': '休息日',
          '2019-12-22': '休息日',
          '2019-07-10': '工作日',
          '2019-09-23': '工作日',
          '2019-08-31': '休息日',
          '2019-05-03': '劳动节',
          '2019-05-11': '休息日',
          '2019-01-31': '工作日',
          '2019-02-24': '休息日',
          '2019-07-02': '工作日',
          '2019-09-06': '工作日',
          '2019-05-14': '工作日',
          '2019-08-13': '工作日',
          '2019-06-01': '休息日',
          '2019-04-01': '工作日',
          '2019-02-11': '工作日',
          '2019-03-28': '工作日',
          '2019-06-07': '端午节',
          '2019-06-04': '工作日',
          '2019-12-23': '工作日',
          '2019-08-30': '工作日',
          '2019-06-27': '工作日',
          '2019-06-15': '休息日',
          '2019-12-28': '休息日',
          '2019-02-21': '工作日',
          '2019-05-25': '休息日',
          '2019-01-26': '休息日',
          '2019-05-09': '工作日',
          '2019-05-05': '工作日',
          '2019-01-20': '休息日',
          '2019-02-06': '春节',
          '2019-03-11': '工作日',
          '2019-03-06': '工作日',
          '2019-04-15': '工作日',
          '2019-12-16': '工作日',
          '2019-05-15': '工作日',
          '2019-06-13': '工作日',
          '2019-08-22': '工作日',
          '2019-06-03': '工作日',
          '2019-03-14': '工作日',
          '2019-04-05': '清明节',
          '2019-09-04': '工作日',
          '2019-07-28': '休息日',
          '2019-07-18': '工作日',
          '2019-08-14': '工作日',
          '2019-12-26': '工作日',
          '2019-10-31': '工作日',
          '2019-03-20': '工作日',
          '2019-01-27': '休息日',
          '2019-05-30': '工作日',
          '2019-01-22': '工作日',
          '2019-09-14': '中秋节',
          '2019-09-19': '工作日',
          '2019-01-08': '工作日',
          '2019-04-11': '工作日',
          '2019-12-18': '工作日',
          '2019-02-02': '工作日',
          '2019-06-10': '工作日',
          '2019-11-02': '休息日',
          '2019-09-22': '休息日',
          '2019-02-22': '工作日',
          '2019-10-05': '国庆节',
          '2019-01-21': '工作日',
          '2019-09-09': '工作日',
          '2019-04-27': '休息日',
          '2019-01-09': '工作日',
          '2019-06-26': '工作日',
          '2019-12-24': '工作日',
          '2019-06-14': '工作日',
          '2019-10-03': '国庆节',
          '2019-03-31': '休息日',
          '2019-09-03': '工作日',
          '2019-08-17': '休息日',
          '2019-12-21': '休息日',
          '2019-03-30': '休息日',
          '2019-06-28': '工作日',
          '2019-02-27': '工作日',
          '2019-06-29': '休息日',
          '2019-11-16': '休息日',
          '2019-03-02': '休息日',
          '2019-01-25': '工作日',
          '2019-05-16': '工作日',
          '2019-08-03': '休息日',
          '2019-03-25': '工作日',
          '2019-11-27': '工作日',
          '2019-11-01': '工作日',
          '2019-08-10': '休息日',
          '2019-09-20': '工作日',
          '2019-01-15': '工作日',
          '2019-08-16': '工作日',
          '2019-10-11': '工作日',
          '2019-12-30': '工作日',
          '2019-04-23': '工作日',
          '2019-02-16': '休息日',
          '2019-09-01': '休息日',
          '2019-11-13': '工作日',
          '2019-12-19': '工作日',
          '2019-12-09': '工作日',
          '2019-03-16': '休息日',
          '2019-07-26': '工作日',
          '2019-05-12': '休息日',
          '2019-07-04': '工作日',
          '2019-02-10': '春节',
          '2019-05-23': '工作日',
          '2019-08-04': '休息日',
          '2019-10-30': '工作日',
          '2019-04-12': '工作日',
          '2019-09-17': '工作日',
          '2019-06-17': '工作日',
          '2019-05-28': '工作日',
          '2019-01-28': '工作日',
          '2019-07-29': '工作日',
          '2019-04-21': '休息日',
          '2019-09-26': '工作日',
          '2019-07-07': '休息日',
          '2019-01-29': '工作日',
          '2019-12-31': '工作日',
          '2019-11-18': '工作日',
          '2019-08-19': '工作日',
          '2019-04-04': '工作日',
          '2019-10-21': '工作日',
          '2019-08-09': '工作日',
          '2019-11-12': '工作日',
          '2019-10-06': '国庆节',
          '2019-01-19': '休息日',
          '2019-06-11': '工作日',
          '2019-06-22': '休息日',
          '2019-12-12': '工作日',
          '2019-08-02': '工作日',
          '2019-04-02': '工作日',
          '2019-07-19': '工作日',
          '2019-01-16': '工作日',
          '2019-06-05': '工作日',
          '2019-09-05': '工作日',
          '2019-07-31': '工作日',
          '2019-11-11': '工作日',
          '2019-05-18': '休息日',
          '2019-12-25': '工作日',
          '2019-01-30': '工作日',
          '2019-10-26': '休息日',
          '2019-08-12': '工作日',
          '2019-08-26': '工作日',
          '2019-11-29': '工作日',
          '2019-11-25': '工作日',
          '2019-09-25': '工作日',
          '2019-12-13': '工作日',
          '2019-12-01': '休息日',
          '2019-11-10': '休息日',
          '2019-03-29': '工作日',
          '2019-07-11': '工作日',
          '2019-07-08': '工作日',
          '2019-08-06': '工作日',
          '2019-10-29': '工作日',
          '2019-07-12': '工作日',
          '2019-07-22': '工作日',
          '2019-09-10': '工作日',
          '2019-06-24': '工作日',
          '2019-02-01': '工作日',
          '2019-02-12': '工作日',
          '2019-10-04': '国庆节',
          '2019-11-24': '休息日',
          '2019-03-01': '工作日',
          '2019-08-07': '工作日',
          '2019-02-17': '休息日',
          '2019-09-18': '工作日',
          '2019-12-02': '工作日',
          '2019-11-05': '工作日',
          '2019-01-17': '工作日',
          '2019-10-10': '工作日',
          '2019-10-01': '国庆节',
          '2019-02-18': '工作日',
          '2019-11-08': '工作日',
          '2019-01-10': '工作日',
          '2019-03-19': '工作日',
          '2019-08-25': '休息日',
          '2019-06-09': '端午节',
          '2019-07-21': '休息日',
          '2019-12-17': '工作日',
          '2019-05-01': '劳动节',
          '2019-03-09': '休息日',
          '2019-08-08': '工作日',
          '2019-04-28': '工作日',
          '2019-10-18': '工作日',
          '2019-09-07': '休息日',
          '2019-09-24': '工作日',
          '2019-11-07': '工作日',
          '2019-03-22': '工作日',
          '2019-10-24': '工作日',
          '2019-10-14': '工作日',
          '2019-06-02': '休息日',
          '2019-02-09': '春节',
          '2019-07-01': '工作日',
          '2019-11-30': '休息日',
          '2019-05-17': '工作日',
          '2019-01-03': '工作日',
          '2019-12-20': '工作日',
          '2019-06-19': '工作日',
          '2019-12-27': '工作日',
          '2019-04-13': '休息日',
          '2019-09-12': '工作日',
          '2019-03-21': '工作日',
          '2019-12-15': '休息日',
          '2019-03-26': '工作日',
          '2019-02-05': '春节',
          '2019-02-20': '工作日',
          '2019-04-14': '休息日',
          '2019-10-23': '工作日',
          '2019-08-29': '工作日',
          '2019-11-20': '工作日',
          '2019-04-29': '工作日',
          '2019-08-24': '休息日',
          '2019-09-28': '休息日',
          '2019-03-12': '工作日',
          '2019-03-08': '工作日',
          '2019-01-14': '工作日',
          '2019-10-28': '工作日',
          '2019-08-20': '工作日',
          '2019-05-13': '工作日',
          '2019-12-03': '工作日',
          '2019-08-01': '工作日',
          '2019-12-29': '休息日',
          '2019-05-26': '休息日',
          '2019-08-11': '休息日',
          '2019-03-24': '休息日',
          '2019-03-13': '工作日',
          '2019-07-06': '休息日',
          '2019-12-06': '工作日',
          '2019-12-05': '工作日',
          '2019-01-02': '工作日',
          '2019-02-04': '春节',
          '2019-03-18': '工作日',
          '2019-09-08': '休息日',
          '2019-01-24': '工作日',
          '2019-06-16': '休息日',
          '2019-03-05': '工作日',
          '2019-11-06': '工作日',
          '2019-07-24': '工作日',
          '2019-04-09': '工作日',
          '2019-08-15': '工作日',
          '2019-09-13': '中秋节',
          '2019-07-14': '休息日',
          '2019-10-09': '工作日',
          '2019-05-29': '工作日',
          '2019-02-28': '工作日',
          '2019-01-13': '休息日',
          '2019-11-26': '工作日',
          '2019-03-07': '工作日',
          '2019-06-06': '工作日',
          '2019-04-16': '工作日',
          '2019-12-04': '工作日',
          '2019-09-21': '休息日',
          '2019-01-05': '休息日',
          '2019-12-08': '休息日',
          '2019-11-04': '工作日',
          '2019-05-20': '工作日',
          '2019-09-16': '工作日',
          '2019-10-19': '休息日',
          '2019-07-16': '工作日',
          '2019-12-10': '工作日',
          '2019-10-25': '工作日',
          '2019-08-05': '工作日',
          '2019-09-27': '工作日',
          '2019-12-11': '工作日',
          '2019-07-25': '工作日',
          '2019-06-18': '工作日',
          '2019-03-04': '工作日',
          '2019-04-26': '工作日',
          '2019-06-21': '工作日',
          '2019-02-19': '工作日',
          '2019-10-15': '工作日',
          '2019-04-10': '工作日',
          '2019-10-17': '工作日',
          '2019-09-02': '工作日',
          '2019-06-08': '端午节',
          '2019-03-17': '休息日',
          '2019-04-24': '工作日',
          '2019-12-07': '休息日',
          '2019-05-19': '休息日',
          '2019-01-23': '工作日',
          '2019-11-09': '休息日',
          '2019-10-08': '工作日',
          '2019-11-23': '休息日',
          '2019-11-03': '休息日',
          '2019-01-01': '元旦',
          '2019-05-04': '劳动节',
          '2019-05-31': '工作日',
          '2019-11-15': '工作日',
          '2019-03-23': '休息日',
          '2019-04-30': '工作日',
          '2019-07-30': '工作日',
          '2019-04-18': '工作日',
          '2019-05-22': '工作日',
          '2019-09-30': '工作日',
          '2019-02-08': '春节',
          '2019-02-26': '工作日',
          '2019-10-27': '休息日',
          '2019-11-21': '工作日',
          '2019-10-16': '工作日',
          '2019-07-05': '工作日',
          '2019-04-03': '工作日',
          '2019-09-29': '工作日',
          '2019-10-07': '国庆节',
          '2019-01-12': '休息日',
          '2019-02-15': '工作日',
          '2019-10-20': '休息日',
          '2019-09-15': '中秋节',
          '2019-03-15': '工作日',
          '2019-07-27': '休息日',
          '2019-11-22': '工作日',
          '2019-05-08': '工作日',
          '2019-08-28': '工作日',
          '2019-04-22': '工作日',
          '2019-04-08': '工作日',
          '2019-07-20': '休息日',
          '2019-01-11': '工作日',
          '2019-01-04': '工作日',
          '2019-01-06': '休息日',
          '2019-04-25': '工作日',
          '2019-04-19': '工作日',
          '2019-06-25': '工作日',
          '2019-05-24': '工作日',
          '2019-05-07': '工作日',
          '2019-08-27': '工作日',
          '2019-05-27': '工作日',
          '2019-05-21': '工作日',
          '2019-05-06': '工作日',
          '2019-03-10': '休息日',
          '2019-04-07': '清明节',
          '2019-03-27': '工作日',
          '2019-10-12': '工作日',
          '2019-02-23': '休息日',
          '2019-12-14': '休息日',
          '2019-07-13': '休息日',
          '2019-02-14': '工作日',
          '2019-01-18': '工作日',
          '2019-06-20': '工作日',
          '2019-04-17': '工作日',
          '2019-06-23': '休息日',
          '2019-02-07': '春节',
          '2019-06-30': '休息日',
          '2019-02-13': '工作日',
          '2019-08-21': '工作日',
          '2019-10-22': '工作日',
          '2019-11-28': '工作日',
          '2019-05-10': '工作日',
          '2019-07-23': '工作日',
          '2019-07-03': '工作日',
          '2019-05-02': '劳动节',
          '2019-06-12': '工作日',
          '2019-11-17': '休息日',
          '2019-04-20': '休息日',
          '2019-08-23': '工作日',
          '2019-11-14': '工作日',
          '2019-07-17': '工作日',
          '2019-04-06': '清明节',
          '2019-10-02': '国庆节',
          '2019-01-07': '工作日'
        }
      }
    },
    mounted () {
      // 获取浏览器可视区域高度
      this.clientHeight = `${document.documentElement.clientHeight}` - 1// document.body.clientWidth;
      this.clientWidth = `${document.documentElement.clientWidth}` - 1
      console.log(this.clientWidth)
      let _this = this
      window.onresize = function temp () {
        _this.clientHeight = `${document.documentElement.clientHeight}` - 1
        _this.clientWidth = `${document.documentElement.clientWidth}` - 1
        console.log(this.clientWidth)
      }
    },
    methods: {
      isaaaa (rowIndex, colIndex) {
        if (this.$refs.table123) {
          let tableData = this.$refs.table123.$refs.tbody._props.data
          return tableData[rowIndex][Object.keys(tableData[rowIndex])[colIndex]].aaaa.length > 0
        } else {
          return false
        }
      },
      isasd (rowIndex, colIndex) {
        if (this.$refs.table123) {
          let tableData = this.$refs.table123.$refs.tbody._props.data
          return tableData[rowIndex][Object.keys(tableData[rowIndex])[colIndex]].aaaa.filter(aa => aa === this.asd).length > 0
        } else {
          return false
        }
      },
      bbb (rowIndex, colIndex) {
        this.asd = '' + rowIndex + ',' + colIndex
        this.qwer = [rowIndex, colIndex]
      },
      isqwe (rowIndex, colIndex) {
        return rowIndex === this.qwer[0] && colIndex === this.qwer[1]
      },
      // qwerr (rowIndex, colIndex) {
      //   this.qwer = [rowIndex, colIndex]
      // },
      getNextWorkDay (startDate, cycle) {
        let dateObj = new Date(startDate)
        while (cycle !== 0) {
          dateObj.setDate(dateObj.getDate() + 1)
          let dateStr = dateObj.getFullYear() + '-' +
            ('0' + (dateObj.getMonth() + 1)).slice(-2) + '-' +
            ('0' + dateObj.getDate()).slice(-2)
          if (this.isWorkdayData[dateStr] === '工作日') {
            cycle--
          }
        }
        return dateObj
      },
      calculationEndDate (rowObj, colIndex) {
        let thisObj = rowObj[Object.keys(rowObj)[colIndex]]
        if (thisObj.startDate && thisObj.cycle) {
          thisObj.endDate = this.getNextWorkDay(thisObj.startDate, thisObj.cycle - 1)
        } else {
          thisObj.endDate = null
        }

        if (thisObj.startDate && ++colIndex < this.columnsData.length) {
          let nextObj = rowObj[Object.keys(rowObj)[colIndex]]
          nextObj.startDate = this.getNextWorkDay(thisObj.startDate, thisObj.cycle)
          this.calculationEndDate(rowObj, colIndex)
        } else {
          this.aaa()
        }

        // console.log(this.$refs.table123.$refs.tbody._props.data)
      },
      aaa () {
        let tableData = this.$refs.table123.$refs.tbody._props.data
        console.log(123)
        for (let i = 0; i < this.tableData.length; i++) {
          for (let j = 1; j < this.columnsData.length; j++) {
            tableData[i][Object.keys(tableData[i])[j]].aaaa = []
          }
        }
        for (let i = 0; i < this.tableData.length; i++) {
          for (let j = 0; j < this.columnsData.length; j++) {
            for (let x = i + 1; x < this.tableData.length; x++) {
              for (let y = 0; y < this.columnsData.length; y++) {
                let obj1 = tableData[i][Object.keys(tableData[i])[j]]
                let obj2 = tableData[x][Object.keys(tableData[x])[y]]

                if (obj1.startDate && obj2.startDate && obj1.endDate && obj2.endDate && obj1.teacher && obj2.teacher) {
                  // console.log(obj1.startDate.valueOf(), obj2.startDate.valueOf())
                  if (obj1.teacher === obj2.teacher) {
                    if (obj2.startDate.valueOf() < obj1.endDate.valueOf()) { // 逻辑仍需补充
                      obj1.aaaa.push('' + x + ',' + y)
                      obj2.aaaa.push('' + i + ',' + j)
                      console.log(obj1, obj2)
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
  .date div {
    margin-bottom: 8px;
  }

  .ccc {
    background-color: rgba(255, 153, 0, 0.3);
  }

  .abb {
    background-color: rgba(255, 153, 0, 8);
  }

  .qwe {
    background-color: rgba(237, 64, 20, 0.9);
  }

  .date /deep/ .el-input-number--mini {
    width: 200px;
    line-height: 30px;
  }

  .date /deep/ .el-input--mini .el-input__inner {
    height: 32px;
    line-height: 32px;
  }

  .date /deep/ .el-input-number--mini .el-input-number__decrease, .date /deep/ .el-input-number--mini .el-input-number__increase {
    width: 32px;
  }

  .date /deep/ .el-input-number__decrease, .date /deep/ .el-input-number__increase {
    background-color: #fff;
  }

  .date /deep/ .ivu-input[disabled], fieldset[disabled] .ivu-input {
    background-color: #fff !important;
    color: #000 !important;
  }

  .home /deep/ .ivu-table-cell {
    padding: 2px;
  }

  .home /deep/ .ivu-table-cell > span {
    padding: 16px;
  }
</style>
