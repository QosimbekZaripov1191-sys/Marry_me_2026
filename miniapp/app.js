const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

const API = "http://localhost:8000/api";
let token = localStorage.getItem("token");

async function telegramAuth() {
  const initData = tg.initData;
  if (!initData) throw new Error("No Telegram initData");

  const r = await fetch(`${API}/telegram`, { // API уже "http://localhost:8000/api" :contentReference[oaicite:2]{index=2}
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ initData }),
  });

  if (!r.ok) throw new Error(await r.text());
  const data = await r.json();

  token = data.access_token;
  localStorage.setItem("token", token);
}

async function init() {
  token = localStorage.getItem("token");
  if (!token) await telegramAuth();

  await loadFeed();
  show("screenFeed");

  // остальной код init без изменений...
}

async function init() {
  if (!token) {
    await telegramAuth();
  }

  document.body.innerHTML = "<h2>✅ Telegram Mini App работает</h2>";
}

init().catch(e => {
  document.body.innerHTML = "<pre>❌ " + e.message + "</pre>";
});