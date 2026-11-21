export default {
  async fetch(request, env) {
    const path = new URL(request.url).pathname;
    if (!/^\/publicacoes\/[0-9a-f]{32}\.(mp4|jpg|jpeg|png|webp)$/.test(path)) {
      return new Response(null, { status: 404 });
    }
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return new Response(null, { status: 405, headers: { Allow: 'GET, HEAD' } });
    }

    const key = path.slice(1);
    const object = await env.MEDIA.head(key);
    const expiresAt = Number(object?.customMetadata?.['expires-at']);
    if (!object || !Number.isFinite(expiresAt) || expiresAt <= Date.now()) {
      return new Response(null, { status: 404 });
    }

    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set('ETag', object.httpEtag);
    headers.set('Cache-Control', 'private, no-store');
    headers.set('Accept-Ranges', 'bytes');
    headers.set('Content-Length', object.size);
    if (request.method === 'HEAD') return new Response(null, { headers });

    let range;
    const requested = request.headers.get('Range');
    if (requested !== null) {
      const parts = /^bytes=(\d*)-(\d*)$/.exec(requested);
      if (parts && (parts[1] || parts[2])) {
        const offset = parts[1] ? Number(parts[1]) : Math.max(0, object.size - Number(parts[2]));
        const end = parts[1] && parts[2] ? Math.min(Number(parts[2]), object.size - 1) : object.size - 1;
        if (Number.isSafeInteger(offset) && offset >= 0 && offset <= end) {
          range = { offset, length: end - offset + 1 };
          headers.set('Content-Range', `bytes ${offset}-${end}/${object.size}`);
          headers.set('Content-Length', range.length);
        }
      }
      if (!range) {
        return new Response(null, {
          status: 416,
          headers: { 'Content-Range': `bytes */${object.size}` },
        });
      }
    }
    const file = await env.MEDIA.get(key, { range });
    if (!file) return new Response(null, { status: 404 });
    return new Response(file.body, { status: range ? 206 : 200, headers });
  },
};
