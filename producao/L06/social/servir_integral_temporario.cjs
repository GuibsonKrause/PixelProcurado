const http = require('node:http');
const fs = require('node:fs');
const { join } = require('node:path');

const route = process.env.L06_REEL_ROUTE;
if (!/^\/[a-f0-9]{40}\/L06\.mp4$/.test(route || '')) throw new Error('Rota temporária inválida');
const path = join(__dirname, 'L06_Instagram_Integral_1080x1920_Leve.mp4');
const { size } = fs.statSync(path);

http.createServer((req, res) => {
  if (req.url !== route || !['HEAD', 'GET'].includes(req.method)) {
    return res.writeHead(404).end();
  }
  const headers = { 'Content-Type': 'video/mp4', 'Accept-Ranges': 'bytes', 'Cache-Control': 'no-store' };
  let start = 0;
  let end = size - 1;
  let status = 200;
  if (req.headers.range) {
    const range = /^bytes=(\d*)-(\d*)$/.exec(req.headers.range);
    if (!range || (!range[1] && !range[2])) return res.writeHead(416, { 'Content-Range': 'bytes */' + size }).end();
    if (range[1]) {
      start = Number(range[1]);
      if (range[2]) end = Math.min(end, Number(range[2]));
    } else {
      start = Math.max(0, size - Number(range[2]));
    }
    if (start > end || start >= size) return res.writeHead(416, { 'Content-Range': 'bytes */' + size }).end();
    status = 206;
    headers['Content-Range'] = 'bytes ' + start + '-' + end + '/' + size;
  }
  headers['Content-Length'] = end - start + 1;
  res.writeHead(status, headers);
  console.log(req.method, status, headers['Content-Length']);
  if (req.method === 'HEAD') return res.end();
  const stream = fs.createReadStream(path, { start, end });
  stream.on('error', () => res.destroy());
  res.on('close', () => stream.destroy());
  stream.pipe(res);
}).listen(18893, '0.0.0.0');
