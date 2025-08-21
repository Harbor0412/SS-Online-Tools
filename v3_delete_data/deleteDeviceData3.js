/**
 * 删除指定时间范围内的数据
 * 1.先执行npm install @influxdata/influxdb-client @influxdata/influxdb-client-apis
 */

const { InfluxDB } = require('@influxdata/influxdb-client');
const { DeleteAPI } = require('@influxdata/influxdb-client-apis');
const { DateTime } = require('luxon');

let url = 'https://tsdb.mocreo.com/';

let tsdbToken = 'DQvId_utUQ9qULybtBz1mk5bQdG6dXGH3nw6coObwrlX1y06cOu4BejR-fjINGVfoJPECvRhT_TE_D1XisKaGQ==';

let org = 'SyncSign'; 
let bucket = 'Mocreo';
const influxDB = new InfluxDB({url, token: tsdbToken });

const deviceSns = ["0030AEA403A3CB00"];

const deleteAPI = new DeleteAPI(influxDB)


// 时间范围（UTC时间）
const start = DateTime.fromFormat('2025-08-14 14:30:00', 'yyyy-MM-dd HH:mm:ss', { zone: 'utc' }).toISO()
const stop  = DateTime.fromFormat('2025-08-14 15:20:00', 'yyyy-MM-dd HH:mm:ss', { zone: 'utc' }).toISO()

async function deleteData(sn) {
  deleteAPI.postDelete({
    org,
    bucket,
    body: {
      start: start,
      stop: stop,
      predicate: `nodeId="${sn}"`,
    },
  }).then(() => {
    console.log('delete tsdb data success');
  }).catch(err => {
    console.error('delete tsdb data error', err);
  })
}

deviceSns.forEach(sn => {
  deleteData(sn);
});