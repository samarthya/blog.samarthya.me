// Hearts for Bhanuni's Studio: one public number per drawing, nothing else.
//
//   GET  /hearts        -> {"c93dhk": 4, "f8swdt": 1, ...}   (every drawing with at least one heart)
//   POST /hearts/<id>   -> {"id": "c93dhk", "n": 5}           (adds one heart)
//
// No names, no messages, no IP addresses are stored: the table has two columns, the drawing id and a count.
// A heart is only accepted for an id that is on the live gallery page, so nobody can fill the table with junk.
// "One heart per drawing per browser" is kept by the page (localStorage); this side only checks the id.

//
// Blog posts get three reactions the same way (no comments, nothing personal):
//
//   GET  /reactions/<slug>          -> {"like": 3, "dislike": 0, "heart": 5}
//   POST /reactions/<slug>/<kind>   -> {"slug": "...", "kind": "like", "n": 4}   (kind: like | dislike | heart)
//
// A reaction is only accepted for a post that is in the live sitemap.

const GALLERY = "https://samarthya.me/bhanuni/";
const SITEMAP = "https://samarthya.me/sitemap.xml";
const ALLOWED_ORIGINS = ["https://samarthya.me", "http://localhost:1313"];
const ID = /^[a-z2-9]{6}$/;
const SLUG = /^[a-z0-9_-]{1,120}$/;
const KINDS = ["like", "dislike", "heart"];
const TTL_MS = 10 * 60 * 1000;

// A set of names scraped from a live page, cached per Worker instance for 10 minutes.
function liveSet(url, pattern) {
  let set = null, at = 0;
  return async () => {
    if (set && Date.now() - at < TTL_MS) return set;
    const text = await (await fetch(url, { cf: { cacheTtl: 600 } })).text();
    set = new Set([...text.matchAll(pattern)].map(m => m[1]));
    at = Date.now();
    return set;
  };
}

// the live gallery is minified, so the attribute may have no quotes: data-id=c93dhk
const galleryIds = liveSet(GALLERY, /data-id="?([a-z2-9]{6})\b/g);
const postSlugs = liveSet(SITEMAP, /<loc>https:\/\/samarthya\.me\/posts\/([a-z0-9_-]+)\/<\/loc>/g);

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

    const r = url.pathname.match(/^\/reactions\/([^/]+)(?:\/([^/]+))?$/);
    if (r && request.method === "GET" && !r[2]) {
      const { results } = await env.DB.prepare("SELECT kind, n FROM reactions WHERE slug = ?1").bind(r[1]).all();
      const counts = Object.fromEntries(KINDS.map(k => [k, 0]));
      for (const row of results) counts[row.kind] = row.n;
      return json(counts, 200, headers);
    }
    if (r && request.method === "POST" && r[2]) {
      if (!ALLOWED_ORIGINS.includes(request.headers.get("Origin"))) return json({ error: "origin" }, 403, headers);
      const [, slug, kind] = r;
      if (!KINDS.includes(kind)) return json({ error: "unknown reaction" }, 404, headers);
      if (!SLUG.test(slug) || !(await postSlugs()).has(slug)) return json({ error: "unknown post" }, 404, headers);
      const row = await env.DB.prepare(
        "INSERT INTO reactions (slug, kind, n) VALUES (?1, ?2, 1) ON CONFLICT(slug, kind) DO UPDATE SET n = n + 1 RETURNING n"
      ).bind(slug, kind).first();
      return json({ slug, kind, n: row.n }, 200, headers);
    }

    return json({ error: "not found" }, 404, headers);
  },
};
