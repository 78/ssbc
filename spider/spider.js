const path = require('path')
const moment = require('moment')
const metadata = require('./metadata')
const Spider = require('dhtspider')
const MongoClient = require('mongodb').MongoClient
const stringHash = require('string-hash')

const MAX_CONCURRENT = parseInt(process.env.MAX_CONCURRENT || 500)
const MAX_HASH_BUFFER = 1000000

let torrentdb = null
let nextTorrentId = 0
MongoClient.connect('mongodb://localhost:27017/admin', {useNewUrlParser: true}, (err, mconn) => {
    if(err) {
        console.error(err)
        process.exit(1)
    }
    torrentdb = mconn.db('torrent')
    torrentdb.collection('log').createIndex({date: 1, reqs: -1})
    torrentdb.collection('log').createIndex({hash: 1})
    torrentdb.collection('hash').createIndex({hash: 1}, {unique: 1})
    torrentdb.collection('hash').find().sort({_id: -1}).limit(1).next((err, r) => {
        nextTorrentId = (r && r._id || 0) + 1
        console.log('Next torrent _id is', nextTorrentId, 'tableCaption', process.env.TABLE_CAPTION)
    })
})


let n_reqs = 0, n_valid= 0, n_new = 0
const visited = [], updates = [], downloading = {}
const spider = new Spider({
    bootstraps: [
        {address: 'router.bittorrent.com', port: 6881}, 
        {address: 'dht.transmissionbt.com', port: 6881},
        {address: 'router.utorrent.com', port: 6881}
    ],
    tableCaption: parseInt(process.env.TABLE_CAPTION || 200)
})

spider.on('ensureHash', (hash, addr) => {
    hash = hash.toLowerCase()
    const visitedKey = stringHash(`${hash}:${addr.address}`)
    if(visited.includes(visitedKey)) {
        return
    }
    visited.push(visitedKey)
    while(visited.length > MAX_HASH_BUFFER)
        visited.shift()

    n_reqs += 1
    const utcnow = moment.utc().toDate()
    const today = moment().format('YYYY-MM-DD')
    if(n_reqs >= 1000) {
        torrentdb.collection('log').bulkWrite(updates)
        updates.length = 0
        torrentdb.collection('spider').updateOne({_id: today}, {
            $inc: {new_hashes: n_new, total_reqs: n_reqs, valid_reqs: n_valid}
            }, {upsert: true})
        console.log('[Report]', new Date(), 
            'n_reqs', n_reqs, 'n_valid', n_valid, 'n_new', n_new, 'n_downloading', Object.keys(downloading).length)
        n_new = n_reqs = n_valid = 0
    }
    
    torrentdb.collection('hash').find({hash: hash}).limit(1).next((err, existingHash) => {
        if(existingHash) {
            n_valid += 1
            updates.push({
                updateOne: {
                    filter: {date: today, hash: hash},
                    update: {$set: {atime: utcnow}, $inc: {reqs: 1}},
                    upsert: true
                }
            })
        }else{
            if(Object.keys(downloading).length >= MAX_CONCURRENT || downloading[hash]) 
                return 
            downloading[hash] = true
            //console.log('[CONNECT]', new Date(), addr, hash)
            metadata.downloadMetadata(hash, addr, (err, data) => {
                delete downloading[hash]
                if(!data)
                    return
                n_valid += 1
                n_new += 1
                const res = metadata.parseMetadata(data)

                /* save filelist to mongodb */
                if(res.files.length > 0) {
                    torrentdb.collection('filelist').replaceOne({_id: hash}, {v: res.files}, {upsert:true})
                }
                /* save hash to db */
                const item = buildNewItem(hash, addr, res)
                torrentdb.collection('hash').insertOne(item, (err, r) => {
                    if(err) {
                        console.error(new Date(), hash, addr, item, err)
                    }else {
                        console.log('[New]', new Date(), item._id, hash, item.name, addr.address, res.files.length)
                    }
                })
            })

        }
    })
})


function buildNewItem(hash, addr, res) {
    const utcnow = moment.utc().toDate()
    const item = {
        _id: nextTorrentId++,
        hash: hash,
        name: res.info.name,
        ip: addr.address,
        len: res.info.length,
        ctime: utcnow,
        atime: utcnow,
        reqs: 1,
    }
    if(res.files.length > 0) {
        const ls = res.files.filter((f) => {return !f.path.startsWith('__')})
        ls.sort((a,b) => b.length - a.length)
        const s = (ls || res.files)[0]['path']
        item.ext = path.extname(s).toLowerCase()
    }else{
        item.ext = path.extname(item.name).toLowerCase()
    }
    if(item.ext.length > 10)
        item.ext = ''

    function getCategory(ext) {
        const t = ext + '.'
        const CATS = {
            "package": ".zip.rar.7z.tar.gz.tgz.iso.dmg.pkg.",
            "image": ".jpg.bmp.jpeg.png.gif.tiff.webp.",
            "music": ".mp3.ape.wav.dts.mdf.flac.wma.aac.m4a.",
            "video": ".avi.mp4.rmvb.m2ts.wmv.mkv.flv.qmv.rm.mov.vob.asf.3gp.mpg.mpeg.m4v.f4v.",
            "document": ".pdf.isz.chm.txt.epub.bc!.doc.ppt.pptx.xls.xlsx.docx.",
            "software": ".exe.app.msi.apk."
        }
        for(const k in CATS) {
            if(CATS[k].indexOf(t) > -1) {
                return k
            }
        }
        return 'other'
    }

    item.cat = getCategory(item.ext)
    return item
}


spider.listen(parseInt(process.env.PORT || 6881))

