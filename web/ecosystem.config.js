module.exports = {
  apps : [{
    name   : "web",
    script : "./server",
    env: {
        NODE_ENV: 'production',
        PORT: 3001,
        BASE_URL: 'http://127.0.0.1:3000'
    }
  }]
}
