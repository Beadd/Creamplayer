const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  
  pluginOptions: {
    electronBuilder: {
      preload: 'src/preload.js',
      nodeIntegration: true
    },
  },
  devServer: {
    proxy: {
      '/api': {
        target: 'http://music.163.com',
        changeOrigin: true,
      },
    },
  },
})
