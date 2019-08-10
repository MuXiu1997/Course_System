<!--suppress JSUnresolvedVariable, CssUnusedSymbol, JSUnusedGlobalSymbols -->
<template>
  <div
    class="case"
    :class="{'duplicate':isDuplicate(col)}"
    @click="clickHandler(`${rowIndex}-${colIndex}`)"
    @dblclick.self="clickHandler('')"
  >
    <template v-if="`${rowIndex}-${colIndex}` === currentEdit">
      <div class="cell">
        开始日期：
        <el-date-picker
          v-model="col.startDate"
          type="date"
          placeholder="选择日期"
          format="yyyy 年 MM 月 dd 日"
          value-format="yyyy-MM-dd"
          @change="changeHandler"
          size="mini"
          class="date-picker"
        >
        </el-date-picker>
      </div>
      <div class="cell">
        结束日期：
        <el-date-picker
          v-model="col.endDate"
          type="date"
          readonly
          format="yyyy 年 MM 月 dd 日"
          value-format="yyyy-MM-dd"
          size="mini"
          class="date-picker"
        >
        </el-date-picker>
      </div>
      <div class="cell">
        周&emsp;&emsp;期：
        <el-input-number
          size="mini"
          v-model="col.duration"
          :min="0"
          @change="changeHandler"
        >
        </el-input-number>
      </div>
      <div class="cell">
        <label>
          讲&emsp;&emsp;师：
          <el-select
            v-model="col.teacher"
            clearable
            popper-append-to-body
            placeholder="请选择"
            size="mini"
            @change="CheckHandler"
          >
            <el-option
              v-for="option in options"
              :key="option"
              :label="option"
              :value="option"
            >
            </el-option>
          </el-select>
        </label>
      </div>
    </template>
    <template v-else>
      <div class="cell">
        开始日期：
        <div class="cell-row">
          <i class="el-icon-date date-info"></i>
          {{format(col.startDate) || '无'}}
        </div>
      </div>
      <div class="cell">
        结束日期：
        <div class="cell-row">
          <i class="el-icon-date date-info"></i>
          {{format(col.endDate) || '无'}}
        </div>
      </div>
      <div class="cell">
        周&emsp;&emsp;期：
        <div class="cell-row text-center">
          {{col.duration}}
        </div>
      </div>
      <div class="cell">
        讲&emsp;&emsp;师：
        <div class="cell-row select">
          {{col.teacher || '无'}}
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { InputNumber, Select, Option, DatePicker } from 'element-ui'

const regexp = new RegExp(/(\d{4})-(\d{2})-(\d{2})/)

export default {
  name: 'ScheduleCell',
  props: {
    rowIndex: Number,
    colIndex: Number,
    col: Object,
    currentEdit: String,
    options: Array
  },
  components: {
    'el-input-number': InputNumber,
    'el-select': Select,
    'el-option': Option,
    'el-date-picker': DatePicker
  },
  methods: {
    format (dateStr) {
      if (dateStr) {
        return dateStr.replace(regexp, '$1 年 $2 月 $3 日')
      }
    },
    isDuplicate (col) {
      return col.conflictArray.length > 0
    },
    clickHandler (value) {
      this.$emit('update:currentEdit', value)
    },
    changeHandler () {
      this.$emit('change')
    },
    CheckHandler () {
      this.$emit('check')
    }
  }
}
</script>

<style scoped>
  .case {
    padding: 20px 18px;
    border-radius: 2.5%;
    cursor: pointer;
  }

  .cell {
    height: 32px;
    margin-bottom: 8px;

  }

  .cell-row {
    line-height: 23px;
    width: 200px;
    display: inline-block;
    border: 1px #DCDFE6 solid;
    border-radius: 4px;
    padding: 4px;
    background-color: white;
  }

  .date-picker {
    width: 200px;
  }

  .date-info {
    width: 23px;
    color: #C0C4CC;
    text-align: center;
  }

  .text-center {
    text-align: center;
  }

  .select {
    padding-left: 15px;
  }

  .case /deep/ .el-input-number--mini {
    width: 200px;
    line-height: 30px;
  }

  .case /deep/ .el-input--mini .el-input__inner {
    height: 32px;
    line-height: 32px;
    width: 200px;
  }

  .case /deep/ .el-input-number__decrease, .case /deep/ .el-input-number__increase {
    background-color: #fff;
    width: 32px;
  }
</style>
