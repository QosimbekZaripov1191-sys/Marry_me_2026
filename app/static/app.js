const API = window.location.origin;

const statusEl = document.getElementById("status");
const logEl = document.getElementById("log");
const meEl = document.getElementById("me");

function log(message) {
  if (logEl) {
    logEl.innerText += `${message}\n`;
  }
  console.log(message);
}

function setStatus(message) {
  if (statusEl) {
    statusEl.innerText = message;
  }
}

function getAccessToken() {
  return localStorage.getItem("access_token");
}

function setAccessToken(token) {
  localStorage.setItem("access_token", token);
}

function clearAccessToken() {
  localStorage.removeItem("access_token");
}

async function loginWithTelegram(tg) {
  const initData = tg?.initData;
  if (!initData) {
    setStatus("Нет initData (открой через кнопку в боте)");
    return null;
  }

  try {
    const response = await fetch(`${API}/api/auth/telegram`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ initData }),
    });

    const text = await response.text();
    log(`POST /api/auth/telegram -> ${response.status}`);
    log(text);

    if (!response.ok) {
      setStatus(`Ошибка авторизации: ${response.status}`);
      return null;
    }

    const data = JSON.parse(text);
    if (!data.access_token) {
      setStatus("Нет access_token в ответе");
      return null;
    }

    setAccessToken(data.access_token);
    setStatus("JWT сохранён ✅");
    return data.access_token;
  } catch (error) {
    setStatus("Ошибка авторизации (fetch)");
    log(`ERR: ${error.message}`);
    return null;
  }
}

async function ensureToken(tg) {
  const token = getAccessToken();
  if (token) {
    setStatus("JWT найден");
    return token;
  }

  return loginWithTelegram(tg);
}

async function loadMe() {
  const token = getAccessToken();
  if (!token) {
    alert("Нет JWT — дождитесь логина");
    return;
  }

  try {
    const response = await fetch(`${API}/api/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    const text = await response.text();
    log(`GET /api/me -> ${response.status}`);
    log(text);

    if (!response.ok) {
      alert(`Ошибка /api/me: ${response.status}`);
      return;
    }

    if (meEl) {
      meEl.innerText = text;
    }
  } catch (error) {
    alert("fetch /api/me error");
    log(`ERR: ${error.message}`);
  }
}

function logout() {
  clearAccessToken();
  setStatus("Вышел");
  if (meEl) {
    meEl.innerText = "";
  }
  if (logEl) {
    logEl.innerText = "";
  }
}

function bindButtons() {
  const btnLogin = document.getElementById("btnLoginTelegram");
  const btnMe = document.getElementById("btnMyProfile");
  const btnLogout = document.getElementById("btnLogout");

  if (btnLogin) {
    btnLogin.onclick = async () => {
      clearAccessToken();
      await ensureToken(window.Telegram?.WebApp);
    };
  }

  if (btnMe) {
    btnMe.onclick = loadMe;
  }

  if (btnLogout) {
    btnLogout.onclick = logout;
  }
}

window.addEventListener("load", async () => {
  const tg = window.Telegram?.WebApp;

  log(`origin: ${window.location.origin}`);
  log(`tg: ${tg ? "yes" : "no"}`);

  if (!tg) {
    setStatus("Открыто не в Telegram WebApp");
    bindButtons();
    return;
  }

  tg.ready();
  tg.expand();

  log(`initData length: ${tg.initData ? tg.initData.length : "NULL"}`);

  bindButtons();
  await ensureToken(tg);
});
