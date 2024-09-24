module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://backend-service.default.svc.cluster.local:8000',
        changeOrigin: true,
        pathRewrite: { '^/api': '' }, 
      },
    },
  },
};

