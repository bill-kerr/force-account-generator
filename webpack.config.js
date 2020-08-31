const path = require('path');

module.exports = {
  entry: './force_account_generator/webapp/static/webapp/main.js',
  output: {
    filename: 'main.min.js',
    path: path.resolve(__dirname, './force_account_generator/webapp/static/webapp/'),
  },
  module: {
    rules: [
      {
        test: /\.m?js$/,
        exclude: /(node_modules)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
            plugins: ['@babel/plugin-proposal-object-rest-spread'],
          },
        },
      },
    ],
  },
};
