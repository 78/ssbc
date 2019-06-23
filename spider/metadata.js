'use strict'

const Protocol = require('bittorrent-protocol')
const ut_metadata = require('ut_metadata')
const net = require('net')
const crypto = require('crypto')
const bencode = require('bencode')
const Iconv = require('iconv').Iconv

function generateId() { 
    return crypto.createHash('sha1').update(`${(new Date).getTime()}:${Math.random()*99999}`).digest()
}


function downloadMetadata(hash, addr, callback) {
    const sock = net.createConnection(addr.port, addr.address)
    sock.setTimeout(5000)
    let metadata = null

    sock.on('timeout', () => {
        if(sock.connecting) {
            callback && callback(null, metadata)
            callback = null
        }
        sock.end()
    })

    sock.on('close', () => {
        callback && callback(null, metadata)
        callback = null
    })

    sock.on('error', () => {
        callback && callback(null, metadata)
        callback = null
        sock.end()
    })

    sock.on('connect', () => {
        const wire = new Protocol()
        sock.pipe(wire).pipe(sock)
        wire.use(ut_metadata())
        wire.handshake(hash, generateId())
        wire.on('handshake', (h, peer) => {
            wire.ut_metadata.fetch()
        })
        wire.ut_metadata.on('warning', (err) => {
            sock.end()
        })
        wire.ut_metadata.on('metadata', m => {
            metadata = m
            callback && callback(null, metadata)
            callback = null
            sock.end()
        })
    })
}


function tryDecode(encoding, s) {
    const langs = [encoding, 'gbk', 'big5', 'SHIFT_JIS', 'Windows-1251', 'KOI8-T', 'EUC-KR']
    if(typeof s == 'number')
        s = s.toString()
    for(const c of langs) {
        const iconv = new Iconv(c, 'utf-8')
        try{
            return iconv.convert(s).toString()
        }catch(e){
            console.log('failed to decode', s.toString('hex'))
        }
    }
    return s.toString(encoding)
}


function decodeString(encoding, d, name) {
    if(d[name + '.utf-8']) {
        return d[name+'.utf-8'].toString('utf8')
    }
    return tryDecode(encoding, d[name])
}

function parseMetadata(metadata) {
    let encoding = 'utf8'
    const info = bencode.decode(metadata).info
    if(!info.name)
        return
    const a = {}, files = []
    a.name = decodeString(encoding, info, 'name')
    if(info.files) {
        a.length = 0
        info.files.forEach((v) => {
            const paths = []
            if(v['path.utf-8']){
                v['path.utf-8'].forEach((p) => {
                    if(typeof p == 'number')
                        p = p.toString()
                    paths.push(p.toString('utf8'))
                })
            }else{
                v.path.forEach((p) => {
                    paths.push(tryDecode(encoding, p))
                })
            }
            files.push({length:v.length, path:paths.join('/')})
            a.length += v.length
        })
    }else{
        a.length = info.length
    }
    a.data_hash = crypto.createHash('md5').update(info.pieces).digest('hex')
    /*
    if(info.source) a.source = decodeString(encoding, info, 'source')
    if(info.publisher) a.publisher = decodeString(encoding, info, 'publisher')
    if(info['publisher-url']) a['publisher-url'] = decodeString(encoding, info, 'publisher-url')
        */
    return {info: a, files: files}
}


if(!module.parent) {
    downloadMetadata(
    "FECA13581347B003A9F3C495C999373E847E24F4", { address: '188.255.114.215', port: 56053 },
        (err, data) => {
        if(data) {
            parseMetadata(data)
        }
    })
}

module.exports = {
    parseMetadata,
    downloadMetadata
}

