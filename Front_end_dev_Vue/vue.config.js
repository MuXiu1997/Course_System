module.exports = {
  publicPath: './',
  outputDir: '../Front_end_Vue',
  productionSourceMap: false,
  devServer: {
    proxy: 'http://127.0.0.1:5000'
  }
}
