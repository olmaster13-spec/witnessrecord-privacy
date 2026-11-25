// Sends the retired domains to the real one with a permanent redirect, so the
// old name stops competing as a duplicate copy of the site and its links count
// for witnesscamera.com. Everything else is served from the static files.
const OLD_HOSTS = new Set(["witnessrecord.app", "www.witnessrecord.app"]);

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (OLD_HOSTS.has(url.hostname)) {
      url.protocol = "https:";
      url.hostname = "witnesscamera.com";
      url.port = "";
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
