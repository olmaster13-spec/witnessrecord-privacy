// The site is static; this only answers /api/usage, the opt-in anonymous
// counts sent by the app. Everything else goes straight to the files.
//
// Nothing identifying is kept: no IP, no device or user ID, no location.
// Each event is a name from a fixed list plus a few short labels, written to
// Workers Analytics Engine, which only ever answers with totals.

const EVENTS = {
  launch: ["source"],
  recording_start: ["source", "viewfinder", "cameras"],
  recording_stop: ["length"],
  first_upload: ["result", "provider"],
  onboarding_step: ["step"],
  onboarding_done: [],
  case_created: [],
  item_added: ["kind"],
  paywall_shown: ["from"],
  pro_started: ["plan"],
};

const LABEL = /^[a-z0-9_.-]{1,24}$/;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname !== "/api/usage") return env.ASSETS.fetch(request);
    if (request.method !== "POST") return new Response(null, { status: 405 });

    let body;
    try {
      const text = await request.text();
      if (text.length > 8192) return new Response(null, { status: 413 });
      body = JSON.parse(text);
    } catch {
      return new Response(null, { status: 400 });
    }

    const app = clean(body.app) ?? "unknown";
    const platform = clean(body.platform) ?? "unknown";
    const events = Array.isArray(body.events) ? body.events.slice(0, 50) : [];
    for (const e of events) {
      const fields = EVENTS[e?.name];
      if (!fields) continue;
      const labels = fields.map((f) => clean(e[f]) ?? "");
      env.USAGE.writeDataPoint({
        indexes: [e.name],
        // blob1 event, blob2 platform, blob3 app version, blob4.. labels
        blobs: [e.name, platform, app, ...labels],
        doubles: [1],
      });
    }
    return new Response(null, { status: 204 });
  },
};

function clean(value) {
  if (typeof value === "number") value = String(value);
  return typeof value === "string" && LABEL.test(value) ? value : null;
}
