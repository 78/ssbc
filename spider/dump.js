const MongoClient = require('mongodb').MongoClient
const crc32 = require('buffer-crc32')

MongoClient.connect('mongodb://localhost:27017/admin', {useNewUrlParser: true}, (err, mconn) => {
    if(err) {
        console.error(err)
        process.exit(1)
    }
    const torrentdb = mconn.db('torrent')
    const stream = torrentdb.collection('hash').find().stream()
    const d = []
    stream.on('error', (err) => {
        console.error(err)
    })
    const catHash = {}
    stream.on('data', (doc) => {
        const name = doc.name.replace(/"/g, '')
        let cat = catHash[doc.cat]
        if(!cat) {
            cat = crc32.unsigned(doc.cat)
            catHash[doc.cat] = cat
        }
        const atime = Math.floor(doc.atime.getTime()/1000)
        const line = `${doc._id},"${name}",${cat},${doc.len},${atime}\n`
        d.push(line)
        if(d.length >= 1000){
            stream.pause()
            process.stdout.write(d.join(''), ()=> {
                d.length = 0
                stream.resume()
            })
        }
    })
    stream.on('finish', () => {
        process.stdout.write(d.join(''), ()=> {
            mconn.close()
        })
    })
})

