/**
 * 格式化文件大小
 * @param {number} bytes 文件大小（字节）
 * @param {number} decimals 小数位数
 * @returns {string} 格式化后的文件大小
 */
export function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes'

  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']

  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
}

/**
 * 格式化日期时间
 * @param {Date|string} date 日期对象或字符串
 * @param {string} format 格式（默认：YYYY-MM-DD HH:mm:ss）
 * @returns {string} 格式化后的日期字符串
 */
export function formatDateTime(date, format = 'YYYY-MM-DD HH:mm:ss') {
  const d = date instanceof Date ? date : new Date(date)

  const pad = (num) => num.toString().padStart(2, '0')

  const replacements = {
    'YYYY': d.getFullYear(),
    'MM': pad(d.getMonth() + 1),
    'DD': pad(d.getDate()),
    'HH': pad(d.getHours()),
    'mm': pad(d.getMinutes()),
    'ss': pad(d.getSeconds())
  }

  return format.replace(/YYYY|MM|DD|HH|mm|ss/g, match => replacements[match])
}