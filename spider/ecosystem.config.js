module.exports = {
  apps : [{
    name   : "spider",
    script : "./spider.js",
    env: {
        PORT: 6881,
        TABLE_CAPTION: 600,
        MAX_CONCURRENT: 500
    },
    cron_restart: "0 */3 * * *"
  },
  {
      name: 'apis',
      script: './apis.js',
      env: {
          PORT: 3000
      }
  },
  {
      name: 'task',
      script: './task.js'
  }
  ]
}
