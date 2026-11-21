// Hearts for Bhanuni's Studio: one public number per drawing, nothing else.
//
//   GET  /hearts        -> {"c93dhk": 4, "f8swdt": 1, ...}   (every drawing with at least one heart)
//   POST /hearts/<id>   -> {"id": "c93dhk", "n": 5}           (adds one heart)
//
// No names, no messages, no IP addresses are stored: the table has two columns, the drawing id and a count.
// A heart is only accepted for an id that is on the live gallery page, so nobody can fill the table with junk.
// "One heart per drawing per browser" is kept by the page (localStorage); this side only checks the id.

const GALLERY = "https://samarthya.me/bhanuni/";
const ALLOWED_ORIGINS = ["https://samarthya.me", "http://localhost:1313"];
const ID = /^[a-z2-9]{6}$/;
const IDS_TTL_MS = 10 * 60 * 1000;

let ids = null, idsAt = 0;   // ids on the live page, cached per Worker instance

async function galleryIds() {
  if (ids && Date.now() - idsAt < IDS_TTL_MS) return ids;
  const html = await (await fetch(GALLERY, { cf: { cacheTtl: 600 } })).text();
  // the live page is minified, so the attribute may have no quotes: data-id=c93dhk
  ids = new Set([...html.matchAll(/data-id="?([a-z2-9]{6})\b/g)].map(m => m[1]));
  idsAt = Date.now();
  return ids;
}

function cors(origin) {
  const h = { "Content-Type": "application/json", "Cache-Control": "no-store", "Vary": "Origin" };
  if (ALLOWED_ORIGINS.includes(origin)) {
    h["Access-Control-Allow-Origin"] = origin;
    h["Access-Control-Allow-Methods"] = "GET, POST";
  }
  return h;
}

const json = (body, status, headers) => new Response(JSON.stringify(body), { status, headers });

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const headers = cors(request.headers.get("Origin") || "");

    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers });

    if (request.method === "GET" && url.pathname === "/hearts") {
      const { results } = await env.DB.prepare("SELECT id, n FROM hearts").all();
      return json(Object.fromEntries(results.map(r => [r.id, r.n])), 200, headers);
    }

    const m = url.pathname.match(/^\/hearts\/([^/]+)$/);
    if (request.method === "POST" && m) {
      if (!ALLOWED_ORIGINS.includes(request.headers.get("Origin"))) return json({ error: "origin" }, 403, headers);
      const id = m[1];
      if (!ID.test(id) || !(await galleryIds()).has(id)) return json({ error: "unknown drawing" }, 404, headers);
      const row = await env.DB.prepare(
        "INSERT INTO hearts (id, n) VALUES (?1, 1) ON CONFLICT(id) DO UPDATE SET n = n + 1 RETURNING n"
      ).bind(id).first();
      return json({ id, n: row.n }, 200, headers);
    }

    return json({ error: "not found" }, 404, headers);
  },
};
