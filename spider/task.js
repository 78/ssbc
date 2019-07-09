const CronJob = require('cron').CronJob
const moment = require('moment')
const assert=require('assert')
const { exec } = require('child_process')

function doTask(date) {
    const env = {DATE: date}
    console.log('DATE=', date)

    const p1 = exec('node reduce.js', {env: env}, (err) => {
        assert.ifError(err)
        const p2 = exec('indexer -c sphinx.conf hash_delta --rotate', {env: env}, (err) => {
            assert.ifError(err)
            const p3 = exec('indexer -c sphinx.conf --merge hash hash_delta --rotate', (err) => {
                assert.ifError(err)
                console.log(new Date(), date, 'task done')
            })
            p3.stdout.pipe(process.stdout)
        })
        p2.stdout.pipe(process.stdout)
    })
    p1.stdout.pipe(process.stdout)
}

/* 每天凌晨1点执行索引任务 */
if(!module.parent) {
    if(process.env.DATE) {
        doTask(process.env.DATE)
    }else{
        const cj = new CronJob('0 0 1 * * *', ()=> {
            console.log(new Date(), 'Starting indexing task in 10 seconds...')
            setTimeout(() => {
                const date = moment().add(-1, 'days').format('YYYY-MM-DD')
                doTask(date)
            }, 10*1000)
        }, null, true)

        console.log(new Date(), 'CronJob started, next task time is', cj.nextDates().toString())
    }
}

