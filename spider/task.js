const CronJob = require('cron').CronJob
const moment = require('moment')
const assert=require('assert')

function doTask() {
    const date = moment().add(-1, 'days').format('YYYY-MM-DD')
    const env = {DATE: date}
    console.log('DATE=', date)

    exec('node reduce.js', {env: env}, (err) => {
        assert.ifError(err)
        exec('indexer -c sphinx.conf hash_delta --rotate', {env: env}, (err) => {
            assert.ifError(err)
            exec('indexer -c sphinx.conf --merge hash hash_delta --rotate', (err) => {
                assert.ifError(err)
                console.log(new Date(), date, 'task done')
            })
        })
    })
}

/* 每天凌晨1点执行索引任务 */
if(!module.parent) {
    const cj = new CronJob('0 0 1 * * *', ()=> {
        console.log(new Date(), 'Starting indexing task in 10 seconds...')
        setTimeout(() => {
            doTask()
        }, 10*1000)
    }, null, true)

    console.log(new Date(), 'CronJob started, next task time is', cj.nextDates().toString())
}

