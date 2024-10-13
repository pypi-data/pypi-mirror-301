const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");
const express = require('express');
const recaptchaKeys = require("./recaptchaKeys.json");

module.exports = {
  entry: "./src/index.js",
  output: {
    filename: "main.js",
    path: path.resolve(__dirname, "build"),
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: path.join(__dirname, "public", "index.html"),
      templateParameters: {
        RECAPTCHA_SITE_KEY: recaptchaKeys.RECAPTCHA_SITE_KEY
      },
    }),
    new CopyWebpackPlugin({
      patterns: [{ from: "public/images", to: "images" }],
    }),
  ],
  devServer: {
    static: {
      directory: path.join(__dirname, "build"),
    },
    port: 3000,
    setupMiddlewares: (middlewares, devServer) => {
      if (!devServer) {
        throw new Error('webpack-dev-server is not defined');
      }
      devServer.app.use(express.json());
      devServer.app.post('/submit', async (req, res) => {
        const data = req.body;
        const token = data["g-recaptcha-token"];
        delete data["g-recaptcha-token"];
        let recaptcha_response = {};
        if (token) {
          const requestHeaders = {
            method: "POST",
            body: `secret=${recaptchaKeys.RECAPTCHA_SECRET_KEY}&response=${token}`, // URL-encoded body
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded', // important for proper format
            },
          };
          let recaptcha = await fetch("https://www.google.com/recaptcha/api/siteverify", requestHeaders);
          recaptcha = await recaptcha.json();
          recaptcha_response = {
            g_recaptcha_score: recaptcha.success ? recaptcha.score : NaN,
          };
        } else {
          recaptcha_response = {
            g_recaptcha_score: NaN,
          };
        }
        res.body = Object.assign(data, recaptcha_response);
        res.status(200).send(res.body);
      });
      return middlewares;
    }
  },
  module: {
    // exclude node_modules
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ["babel-loader"],
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.svg$/,
        loader: "svg-inline-loader",
      },
    ],
  },
  // pass all js files through Babel
  resolve: {
    extensions: ["*", ".js", ".jsx"],
  },
};
