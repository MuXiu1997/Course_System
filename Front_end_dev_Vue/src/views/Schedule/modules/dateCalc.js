let isWorkdayData

function calculationDate (row, colIndex) {
  for (let i = colIndex; i < row.length; i++) {
    if (row[i].startDate) {
      if (row[i].duration) {
        row[i].endDate = getNextWorkDay(row[i].startDate, row[i].duration - 1)
      } else {
        row[i].endDate = ''
      }
      if (i !== row.length - 1) {
        row[i + 1].startDate = getNextWorkDay(row[i].startDate, row[i].duration)
      }
    } else {
      row[i].endDate = ''
      return
    }
  }
}

function getNextWorkDay (startDate, duration) {
  let dateObj = new Date(startDate)
  let dateStr = formatDate(dateObj)
  while (duration !== 0) {
    dateObj.setDate(dateObj.getDate() + 1)
    dateStr = formatDate(dateObj)
    if (typeof isWorkdayData[dateStr] === 'undefined') {
      alert('工作日数据获取错误')
      return
    }
    if (isWorkdayData[dateStr]) {
      duration--
    }
  }
  return dateStr
}

function formatDate (date) {
  return date.getFullYear() + '-' +
    ('0' + (date.getMonth() + 1)).slice(-2) + '-' +
    ('0' + date.getDate()).slice(-2)
}

function setWorkdayData (obj) {
  isWorkdayData = obj
}

function duplicateChecking (tdArray) {
  let tempArray = []
  for (let i = 0; i < tdArray.length; i++) {
    for (let j = 0; j < tdArray[i].length; j++) {
      tdArray[i][j].conflictArray = []
      tempArray.push({ index: `${i}-${j}`, data: tdArray[i][j] })
    }
  }
  tempArray.sort((a, b) => {
    if (a.data.startDate && b.data.startDate) {
      if (a.data.startDate > b.data.startDate) {
        return 1
      } else if (a.data.startDate < b.data.startDate) {
        return -1
      } else {
        return 0
      }
    } else if (a.data.startDate) {
      return -1
    } else if (b.data.startDate) {
      return 1
    } else {
      return 0
    }
  })
  for (let i = 0; i < tempArray.length - 1; i++) {
    for (let j = i + 1; j < tempArray.length; j++) {
      if (!(tempArray[i].data.teacher && tempArray[j].data.teacher)) {
        continue
      }
      if (tempArray[i].data.teacher !== tempArray[j].data.teacher) {
        continue
      }
      if (!(tempArray[i].data.startDate && tempArray[j].data.startDate)) {
        break
      }
      if (tempArray[i].data.endDate) {
        if (tempArray[j].data.startDate <= tempArray[i].data.endDate) {
          tempArray[i].data.conflictArray.push(tempArray[j].index)
          tempArray[j].data.conflictArray.push(tempArray[i].index)
        } else {
          break
        }
      }
    }
  }
}

export {
  calculationDate,
  setWorkdayData,
  duplicateChecking
}
