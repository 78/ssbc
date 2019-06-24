const MongoClient = require('mongodb').MongoClient
const crc32 = require('buffer-crc32')


const catHash = {}
function printHashes(docs, callback) {
    const d = []
    for(const item of docs) {
        const doc = item.info[0]
        const name = doc.name.replace(/"/g, '')
        let cat = catHash[doc.cat]
        if(!cat) {
            cat = crc32.unsigned(doc.cat)
            catHash[doc.cat] = cat
        }
        const atime = Math.floor(doc.atime.getTime()/1000)
        const line = `${doc._id},"${name}",${cat},${doc.len},${atime}\n`
        d.push(line)
    }
    if(d.length > 0){
        process.stdout.write(d.join(''), () => {
            callback()
        })
    }
}


MongoClient.connect('mongodb://localhost:27017/admin', {useNewUrlParser: true}, (err, mconn) => {
    if(err) {
        console.error(err)
        process.exit(1)
    }
    const torrentdb = mconn.db('torrent')

    if(!process.env.DATE) {
        console.error('env DATE is empty')
        process.exit(1)
    }
    console.error(new Date(), 'dumping data on', process.env.DATE)
    const stream = torrentdb.collection('log').aggregate([
        {
            $match: {date: process.env.DATE}
        },{
            $project: {_id: 0, hash: 1}
        },{
            $lookup: {
                from: 'hash',
                localField: 'hash',
                foreignField: 'hash',
                as: 'info'
            }
        }])
    const d = []
    let ii = 0
    stream.on('data', (doc) => {
        d.push(doc)
        ii += 1
        if(d.length >= 10000){
            stream.pause()
            printHashes(d, ()=> {
                d.length = 0
                stream.resume()
            })
        }
    })
    stream.on('finish', () => {
        printHashes(d, ()=> {
            mconn.close()
        })
    })
})

