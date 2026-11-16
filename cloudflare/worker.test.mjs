import assert from "node:assert/strict";
import { test } from "node:test";
import worker from "./worker.mjs";

const origin = "https://administradorgeral.github.io";

function makeEnv(overrides = {}) {
  return {
    ALLOWED_ORIGIN: origin,
    GEMINI_API_KEY: "test-key-not-real",
    AI_RATE_LIMITER: { limit: async () => ({ success: true }) },
    ...overrides
  };
}

test("rejects requests from origins other than GitHub Pages", async () => {
  const response = await worker.fetch(
    new Request("https://worker.example/api/argon", {
      method: "POST",
      headers: { Origin: "https://attacker.example" }
    }),
    makeEnv()
  );

  assert.equal(response.status, 403);
  assert.deepEqual(await response.json(), { error: "Origem não autorizada." });
});

test("returns rate-limit errors without calling Gemini", async () => {
  const previousFetch = globalThis.fetch;
  globalThis.fetch = async () => {
    assert.fail("Gemini must not be called after rate limiting");
  };

  try {
    const response = await worker.fetch(
      new Request("https://worker.example/api/argon", {
        method: "POST",
        headers: { Origin: origin, "Content-Type": "application/json" },
        body: JSON.stringify({ contents: [{ role: "user", parts: [{ text: "oi" }] }] })
      }),
      makeEnv({ AI_RATE_LIMITER: { limit: async () => ({ success: false }) } })
    );

    assert.equal(response.status, 429);
  } finally {
    globalThis.fetch = previousFetch;
  }
});

test("proxies valid prompts using the fixed Gemini model", async () => {
  const previousFetch = globalThis.fetch;
  let upstreamUrl;
  let upstreamPayload;
  globalThis.fetch = async (url, options) => {
    upstreamUrl = String(url);
    upstreamPayload = JSON.parse(options.body);
    return new Response(JSON.stringify({
      candidates: [{ content: { parts: [{ text: "Resposta Gemini" }] } }]
    }), { status: 200, headers: { "Content-Type": "application/json" } });
  };

  try {
    const response = await worker.fetch(
      new Request("https://worker.example/api/argon", {
        method: "POST",
        headers: { Origin: origin, "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "attacker-selected-model",
          contents: [{ role: "user", parts: [{ text: "pergunta" }] }]
        })
      }),
      makeEnv()
    );

    assert.equal(response.status, 200);
    assert.match(upstreamUrl, /models\/gemini-4-argon:generateContent/);
    assert.equal(upstreamPayload.model, undefined);
    assert.equal((await response.json()).candidates[0].content.parts[0].text, "Resposta Gemini");
  } finally {
    globalThis.fetch = previousFetch;
  }
});

test("fails explicitly when the Gemini secret is missing", async () => {
  const response = await worker.fetch(
    new Request("https://worker.example/api/argon", {
      method: "POST",
      headers: { Origin: origin, "Content-Type": "application/json" },
      body: JSON.stringify({ contents: [{ role: "user", parts: [{ text: "oi" }] }] })
    }),
    makeEnv({ GEMINI_API_KEY: "" })
  );

  assert.equal(response.status, 503);
});
