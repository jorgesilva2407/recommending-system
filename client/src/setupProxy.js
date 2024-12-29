// src/setupProxy.js
const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/api/recommend",
    createProxyMiddleware({
      target: process.env.REACT_APP_RECOMMENDATION_API_URL,
      changeOrigin: true,
      logLevel: "debug",
    })
  );
};
