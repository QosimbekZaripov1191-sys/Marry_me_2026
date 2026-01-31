window.onload = () => {
  const API = window.location.origin;

  const statusEl = document.getElementById("status");
  const logEl = document.getElementById("log");
  const meEl = document.getElementById("me");

  function log(msg) {
    if (logEl) logEl.innerText += msg + "\n";
    console.log(msg);
  }

  // Telegram WebApp
  const tg = window.Telegram?.WebApp;

  log(`origin: ${window.location.origin}`);
  log(`tg: ${tg ? "yes" : "no"}`);

  if (!tg) {
    if (statusEl) statusEl.innerText = "Открыто не в Telegram WebApp";
    return;
  }

  tg.ready();
  tg.expand();

  log(`initData length: ${tg.initData ? tg.initData.length : "NULL"}`);

  async function autoLogin() {
    const token = localStorage.getItem("access_token");
    if (token) {
      if (statusEl) statusEl.innerText = "JWT найден";
      return;
    }

    const initData = tg.initData;
    if (!initData) {
      if (statusEl) statusEl.innerText = "Нет initData (открой через кнопку в боте)";
      return;
    }

    try {
      const res = await fetch(`${API}/api/auth/telegram`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ initData }),
      });

      const text = await res.text();
      log("POST /api/auth/telegram -> " + res.status);
      log(text);

      if (!res.ok) {
        if (statusEl) statusEl.innerText = "Ошибка авторизации: " + res.status;
        return;
      }

      const data = JSON.parse(text);
      if (!data.access_token) {
        if (statusEl) statusEl.innerText = "Нет access_token в ответе";
        return;
      }

      localStorage.setItem("access_token", data.access_token);
      if (statusEl) statusEl.innerText = "JWT сохранён ✅";
    } catch (e) {
      if (statusEl) statusEl.innerText = "Ошибка авторизации (fetch)";
      log("ERR: " + e.message);
    }
  }

  async function loadMe() {
    const token = localStorage.getItem("access_token");
    if (!token) {
      alert("Нет JWT — нажми Login Telegram");
      return;
    }

    try {
      const res = await fetch(`${API}/api/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      const text = await res.text();
      log("GET /api/me -> " + res.status);
      log(text);

      if (!res.ok) {
        alert("Ошибка /api/me: " + res.status);
        return;
      }

      if (meEl) meEl.innerText = text;
    } catch (e) {
      alert("fetch /api/me error");
      log("ERR: " + e.message);
    }
  }

  function logout() {
    localStorage.removeItem("access_token");
    if (statusEl) statusEl.innerText = "Вышел";
    if (meEl) meEl.innerText = "";
    if (logEl) logEl.innerText = "";
  }

  // Кнопки
  const btnLogin = document.getElementById("btnLoginTelegram");
  const btnMe = document.getElementById("btnMyProfile");
  const btnLogout = document.getElementById("btnLogout");

  if (btnLogin) btnLogin.onclick = async () => {
    localStorage.removeItem("access_token");
    await autoLogin();
  };

  if (btnMe) btnMe.onclick = loadMe;
  if (btnLogout) btnLogout.onclick = logout;

  // Автовход
  autoLogin();
};