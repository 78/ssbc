const MongoClient = require('mongodb').MongoClient

MongoClient.connect('mongodb://localhost:27017/admin', {useNewUrlParser: true}, (err, mconn) => {
    if(err) {
        console.error(err)
        process.exit(1)
    }
    const torrentdb = mconn.db('torrent')
    const stream = torrentdb.collection('log').find({date: process.env.DATE}).stream()
    const d = []
    let ii = 0
    stream.on('error', (err) => {
        console.error(err)
    })
    stream.on('data', (doc) => {
        d.push({
            updateOne: {
                filter: {hash: doc._id},
                update: {$set: {atime: doc.atime}, $inc: {reqs: doc.reqs}}
            }
        })
        ii += 1
        if(d.length >= 100000) {
            stream.pause()
            console.log(ii)
            torrentdb.collection('hash').bulkWrite(d, (err, r) => {
                if(err) {
                    console.error(err)
                }else{
                    d.length = 0
                    stream.resume()
                }
            })
        }
    })
    stream.on('finish', () => {
        if(d.length > 0) {
            torrentdb.collection('hash').bulkWrite(d, (err) => {
                if(err) {
                    console.error(err)
                }else{
                    console.log('done', process.env.DATE)
                    mconn.close()
                }
            })
        }
    })
})

