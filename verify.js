// Witness evidence checker. Everything runs in this browser tab: files are
// read locally and never uploaded anywhere. There is no server side.
//
// What it checks, for any mix of dropped files:
//   1. Each .tsr time-stamp proof: that it is a genuine RFC 3161 token signed
//      by FreeTSA (signature verified against the certificate inside it,
//      which must match FreeTSA's published certificate), and which file it
//      covers (the token names the SHA-256 of exactly one manifest or record).
//   2. Each manifest.json / record.json: whether a dropped proof covers it,
//      byte for byte.
//   3. Each video, photo or audio file: its SHA-256, and whether a dropped
//      manifest or record lists that exact hash.
"use strict";

// SHA-256 of FreeTSA's TSA signing certificate (www.freetsa.org/files/tsa.crt),
// valid until 2040. Pinned so a token signed by any other key is not shown as
// trusted.
const FREETSA_CERT_SHA256 = "32e841a95cc1164101ffde41298ef2fc75c1c4372ef095e88a6bbd47dfb191fc";

// ---------- streaming SHA-256 (for files too large to hold in memory) ----------

const K = new Uint32Array([
  0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
  0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
  0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
  0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
  0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
  0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
  0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
  0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2]);

class Sha256 {
  constructor() {
    this.h = new Uint32Array([0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]);
    this.buf = new Uint8Array(64); this.bufLen = 0; this.total = 0; this.w = new Uint32Array(64);
  }
  block(b, o) {
    const w = this.w, h = this.h;
    for (let i = 0; i < 16; i++) w[i] = (b[o+4*i]<<24)|(b[o+4*i+1]<<16)|(b[o+4*i+2]<<8)|b[o+4*i+3];
    for (let i = 16; i < 64; i++) {
      const a = w[i-15], c = w[i-2];
      const s0 = ((a>>>7)|(a<<25)) ^ ((a>>>18)|(a<<14)) ^ (a>>>3);
      const s1 = ((c>>>17)|(c<<15)) ^ ((c>>>19)|(c<<13)) ^ (c>>>10);
      w[i] = (w[i-16] + s0 + w[i-7] + s1) | 0;
    }
    let A=h[0],B=h[1],C=h[2],D=h[3],E=h[4],F=h[5],G=h[6],H=h[7];
    for (let i = 0; i < 64; i++) {
      const S1 = ((E>>>6)|(E<<26)) ^ ((E>>>11)|(E<<21)) ^ ((E>>>25)|(E<<7));
      const t1 = (H + S1 + ((E&F) ^ (~E&G)) + K[i] + w[i]) | 0;
      const S0 = ((A>>>2)|(A<<30)) ^ ((A>>>13)|(A<<19)) ^ ((A>>>22)|(A<<10));
      const t2 = (S0 + ((A&B) ^ (A&C) ^ (B&C))) | 0;
      H=G; G=F; F=E; E=(D+t1)|0; D=C; C=B; B=A; A=(t1+t2)|0;
    }
    h[0]+=A; h[1]+=B; h[2]+=C; h[3]+=D; h[4]+=E; h[5]+=F; h[6]+=G; h[7]+=H;
  }
  update(data) {
    let i = 0; this.total += data.length;
    if (this.bufLen) {
      while (i < data.length && this.bufLen < 64) this.buf[this.bufLen++] = data[i++];
      if (this.bufLen === 64) { this.block(this.buf, 0); this.bufLen = 0; }
    }
    for (; i + 64 <= data.length; i += 64) this.block(data, i);
    while (i < data.length) this.buf[this.bufLen++] = data[i++];
  }
  hex() {
    const bits = this.total * 8;
    const pad = new Uint8Array(((this.bufLen < 56) ? 56 : 120) - this.bufLen + 8);
    pad[0] = 0x80;
    const hi = Math.floor(bits / 0x100000000), lo = bits >>> 0;
    const n = pad.length;
    pad[n-8]=hi>>>24; pad[n-7]=hi>>>16; pad[n-6]=hi>>>8; pad[n-5]=hi;
    pad[n-4]=lo>>>24; pad[n-3]=lo>>>16; pad[n-2]=lo>>>8; pad[n-1]=lo;
    this.update(pad);
    return Array.from(this.h, x => (x >>> 0).toString(16).padStart(8, "0")).join("");
  }
}

async function sha256File(file, onProgress) {
  const hasher = new Sha256();
  const step = 8 * 1024 * 1024;
  for (let pos = 0; pos < file.size; pos += step) {
    const chunk = new Uint8Array(await file.slice(pos, pos + step).arrayBuffer());
    hasher.update(chunk);
    if (onProgress) onProgress(Math.min(1, (pos + step) / file.size));
  }
  return hasher.hex();
}

const hex = buf => Array.from(new Uint8Array(buf), b => b.toString(16).padStart(2, "0")).join("");
const digest = async (alg, bytes) => hex(await crypto.subtle.digest(alg, bytes));

// ---------- minimal DER reader ----------

function readTLV(b, o) {
  const tag = b[o]; let len = b[o+1], hdr = 2;
  if (len & 0x80) {
    const n = len & 0x7f; len = 0;
    for (let i = 0; i < n; i++) len = len * 256 + b[o+2+i];
    hdr = 2 + n;
  }
  return { tag, start: o, hdr, len, body: o + hdr, end: o + hdr + len };
}
function children(b, node) {
  const out = []; let o = node.body;
  while (o < node.end) { const c = readTLV(b, o); out.push(c); o = c.end; }
  return out;
}
const bytesOf = (b, n) => b.subarray(n.start, n.end);
const bodyOf = (b, n) => b.subarray(n.body, n.end);
function oid(b, n) {
  const v = bodyOf(b, n); const parts = [Math.floor(v[0] / 40), v[0] % 40]; let x = 0;
  for (let i = 1; i < v.length; i++) { x = x * 128 + (v[i] & 0x7f); if (!(v[i] & 0x80)) { parts.push(x); x = 0; } }
  return parts.join(".");
}
const HASHES = { "2.16.840.1.101.3.4.2.1": "SHA-256", "2.16.840.1.101.3.4.2.2": "SHA-384",
                 "2.16.840.1.101.3.4.2.3": "SHA-512", "1.3.14.3.2.26": "SHA-1" };
const SIG_HASH = { "1.2.840.113549.1.1.11": "SHA-256", "1.2.840.113549.1.1.12": "SHA-384",
                   "1.2.840.113549.1.1.13": "SHA-512", "1.2.840.10045.4.3.2": "SHA-256",
                   "1.2.840.10045.4.3.3": "SHA-384", "1.2.840.10045.4.3.4": "SHA-512" };
const CURVES = { "1.2.840.10045.3.1.7": ["P-256", 32], "1.3.132.0.34": ["P-384", 48], "1.3.132.0.35": ["P-521", 66] };

/// CMS carries ECDSA signatures as DER SEQUENCE { r, s }; WebCrypto wants the
/// two numbers as fixed-width big-endian halves.
function ecdsaRaw(der, size) {
  const [r, s] = children(der, readTLV(der, 0)).map(n => {
    let v = bodyOf(der, n);
    while (v.length > size && v[0] === 0) v = v.subarray(1);
    const out = new Uint8Array(size); out.set(v, size - v.length); return out;
  });
  const raw = new Uint8Array(size * 2); raw.set(r, 0); raw.set(s, size); return raw;
}

function genTime(b, n) {
  const s = new TextDecoder().decode(bodyOf(b, n)); // YYYYMMDDHHMMSS[.fff]Z
  return new Date(Date.UTC(+s.slice(0,4), +s.slice(4,6)-1, +s.slice(6,8), +s.slice(8,10), +s.slice(10,12), +s.slice(12,14)));
}

/// Parses and verifies an RFC 3161 reply. Returns what it proves, or throws.
async function verifyToken(buf) {
  const b = new Uint8Array(buf);
  const resp = readTLV(b, 0);
  const [status, token] = children(b, resp);
  const statusCode = b[children(b, status)[0].body];
  if (statusCode > 1 || !token) throw new Error("the authority did not grant this time-stamp");
  const [ctype, ctx] = children(b, token);
  if (oid(b, ctype) !== "1.2.840.113549.1.7.2") throw new Error("not a signed time-stamp token");
  const sd = children(b, children(b, ctx)[0]);
  const encap = sd[2];
  const tstOctets = children(b, children(b, encap)[1])[0];
  const tstBytes = bodyOf(b, tstOctets);
  const certsNode = sd.find(n => n.tag === 0xa0);
  const signerInfos = sd[sd.length - 1];
  const si = children(b, children(b, signerInfos)[0]);

  // TSTInfo: version, policy, messageImprint, serial, genTime, ...
  const tb = tstBytes, tst = children(tb, readTLV(tb, 0));
  const imprint = children(tb, tst[2]);
  const imprintAlg = HASHES[oid(tb, children(tb, imprint[0])[0])];
  const imprintHex = hex(bodyOf(tb, imprint[1]));
  const time = genTime(tb, tst[4]);

  // SignerInfo: version, sid, digestAlgorithm, [0] signedAttrs, sigAlg, signature
  const digestAlg = HASHES[oid(b, children(b, si[2])[0])];
  const attrsNode = si.find(n => n.tag === 0xa0);
  const sigAlgNode = si[si.indexOf(attrsNode) + 1];
  const sigNode = si[si.indexOf(attrsNode) + 2];
  let messageDigest = null;
  for (const attr of children(b, attrsNode)) {
    const [t, vals] = children(b, attr);
    if (oid(b, t) === "1.2.840.113549.1.9.4") messageDigest = hex(bodyOf(b, children(b, vals)[0]));
  }
  if (messageDigest !== await digest(digestAlg, tstBytes))
    throw new Error("the token's content does not match its signature");

  // The signing certificate must be FreeTSA's own.
  let spki = null;
  for (const cert of certsNode ? children(b, certsNode) : []) {
    if (await digest("SHA-256", bytesOf(b, cert)) !== FREETSA_CERT_SHA256) continue;
    const tbs = children(b, children(b, cert)[0]);
    const off = tbs[0].tag === 0xa0 ? 1 : 0;
    spki = new Uint8Array(bytesOf(b, tbs[off + 5]));
  }
  if (!spki) throw new Error("signed by an authority this page doesn't recognise; check it with openssl instead");

  const sigAlgOid = oid(b, children(b, sigAlgNode)[0]);
  const sigHash = SIG_HASH[sigAlgOid] || digestAlg;
  const signed = new Uint8Array(bytesOf(b, attrsNode)); signed[0] = 0x31; // [0] IMPLICIT -> SET
  const signature = bodyOf(b, sigNode);
  const spkiAlg = children(spki, readTLV(spki, 0))[0];
  const [keyOid, keyParam] = children(spki, spkiAlg);
  let ok;
  if (oid(spki, keyOid) === "1.2.840.10045.2.1") {
    const [curve, size] = CURVES[oid(spki, keyParam)] || [];
    if (!curve) throw new Error("the signing key uses an unsupported curve");
    const key = await crypto.subtle.importKey("spki", spki, { name: "ECDSA", namedCurve: curve }, false, ["verify"]);
    ok = await crypto.subtle.verify({ name: "ECDSA", hash: sigHash }, key, ecdsaRaw(signature, size), signed);
  } else {
    const key = await crypto.subtle.importKey("spki", spki, { name: "RSASSA-PKCS1-v1_5", hash: sigHash }, false, ["verify"]);
    ok = await crypto.subtle.verify("RSASSA-PKCS1-v1_5", key, signature, signed);
  }
  if (!ok) throw new Error("the signature is not valid");
  return { time, imprintAlg, imprintHex };
}

// ---------- the page ----------

const $ = s => document.querySelector(s);
const results = $("#results");
let busy = false;

function row(kind, title, detail, state) {
  const li = document.createElement("li");
  li.className = "vrow " + state;
  li.innerHTML = `<span class="vicon" aria-hidden="true"></span><div><div class="vtitle"></div><div class="vdetail"></div></div>`;
  li.querySelector(".vtitle").textContent = title;
  li.querySelector(".vdetail").textContent = detail;
  li.dataset.kind = kind;
  results.appendChild(li);
  return li;
}

function hashesIn(json) {
  const out = [];
  if (typeof json.sha256 === "string") out.push({ hash: json.sha256, label: json.fileName || "the recorded file" });
  for (const c of json.chunks || []) if (c.sha256) out.push({ hash: c.sha256, label: `segment ${c.index} (${c.camera}${c.kind === "lowRes" ? ", low-resolution stand-in" : ""})` });
  for (const m of json.mergedVideos || []) if (m.sha256) out.push({ hash: m.sha256, label: `${m.fileName} (full ${m.camera} video)` });
  return out;
}

async function check(files) {
  if (busy) return; busy = true;
  results.innerHTML = ""; $("#summary").textContent = "";
  const proofs = [], records = [], media = [];
  for (const f of files) {
    const name = f.name.toLowerCase();
    if (name.endsWith(".tsr")) proofs.push(f);
    else if (name.endsWith(".json")) records.push(f);
    else media.push(f);
  }

  const stamped = []; // {imprintHex, time, proofName}
  for (const f of proofs) {
    try {
      const t = await verifyToken(await f.arrayBuffer());
      stamped.push({ ...t, proofName: f.name });
    } catch (e) {
      row("proof", f.name, "Not a valid proof: " + e.message + ".", "bad");
    }
  }

  const listed = []; // {hash, label, recordName, stampedAt}
  for (const f of records) {
    const bytes = new Uint8Array(await f.arrayBuffer());
    const sha = await digest("SHA-256", bytes);
    let json; try { json = JSON.parse(new TextDecoder().decode(bytes)); } catch { json = null; }
    if (!json) { row("record", f.name, "Not a Witness manifest or record.", "bad"); continue; }
    const proof = stamped.find(s => s.imprintHex === sha);
    if (proof) {
      proof.used = true;
      row("record", f.name, `Unchanged since ${proof.time.toUTCString()}. Proven by ${proof.proofName}, an RFC 3161 time-stamp signed by FreeTSA.`, "good");
    } else if (stamped.length) {
      row("record", f.name, "None of the proofs you added covers this file. Either it was edited after it was time-stamped, or its own proof is missing.", "bad");
    } else {
      row("record", f.name, "Readable, but no time-stamp proof was added for it, so when it was made can't be confirmed. Add the .tsr file that came with it.", "warn");
    }
    for (const h of hashesIn(json)) listed.push({ ...h, recordName: f.name, stampedAt: proof && proof.time });
  }
  for (const s of stamped.filter(s => !s.used)) {
    row("proof", s.proofName, `Genuine FreeTSA time-stamp from ${s.time.toUTCString()}. Add the manifest or record it belongs to, to see what it covers.`, "warn");
  }

  for (const f of media) {
    const li = row("media", f.name, "Computing fingerprint… 0%", "pending");
    const sha = await sha256File(f, p => li.querySelector(".vdetail").textContent = `Computing fingerprint… ${Math.round(p * 100)}%`);
    const match = listed.find(l => l.hash.toLowerCase() === sha);
    li.className = "vrow " + (match ? (match.stampedAt ? "good" : "warn") : (listed.length ? "bad" : "warn"));
    li.querySelector(".vdetail").textContent = match
      ? `Identical to ${match.label} in ${match.recordName}` + (match.stampedAt ? `, which existed unchanged by ${match.stampedAt.toUTCString()}.` : ". Add its time-stamp proof to confirm when.")
      : (listed.length ? `Not listed in the manifests you added. It isn't one of the original files, or it was altered or re-encoded (sending through a messaging app re-encodes video). SHA-256 ${sha}`
                       : `SHA-256 ${sha}. Add the manifest or record to compare it.`);
  }

  const good = results.querySelectorAll(".good").length, bad = results.querySelectorAll(".bad").length;
  $("#summary").textContent = bad ? `${bad} problem${bad > 1 ? "s" : ""} found.` : good ? "Everything you added checks out." : "";
  busy = false;
}

const drop = $("#drop"), input = $("#files");
input.addEventListener("change", () => check([...input.files]));
drop.addEventListener("dragover", e => { e.preventDefault(); drop.classList.add("over"); });
drop.addEventListener("dragleave", () => drop.classList.remove("over"));
drop.addEventListener("drop", e => { e.preventDefault(); drop.classList.remove("over"); check([...e.dataTransfer.files]); });

if (typeof module !== "undefined") module.exports = { Sha256, verifyToken };
