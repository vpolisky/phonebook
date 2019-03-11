module.exports = {
  runtimeCompiler: undefined,

  devServer: {
    port: 3000,
    proxy: {
      '^/api': {
        target: 'http://localhost:8000'
      }
    }
  },

  publicPath: undefined,
  outputDir: undefined,
  assetsDir: undefined,
  productionSourceMap: undefined,
  parallel: undefined,
  css: undefined
}
