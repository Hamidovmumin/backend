// Animasiya
  (() => {
    const canvas = document.getElementById('bg');

    if (!canvas) return;

    const shouldReduceMotion =
      window.matchMedia('(prefers-reduced-motion: reduce)').matches ||
      window.matchMedia('(max-width: 480px)').matches;

    if (shouldReduceMotion) {
      canvas.style.display = 'none';
      return;
    }

    const ctx = canvas.getContext('2d');

    let W;
    let H;
    let particles = [];
    let orbs = [];
    let startTime = null;
    let lastFrame = 0;

    function resizeCanvas() {
      W = canvas.width = window.innerWidth;
      H = canvas.height = window.innerHeight;
    }

    function makeOrbs() {
      return [
        { x: W * 0.14, y: H * 0.20, r: 360, hue: 38, sat: 88, lig: 68, speed: 0.00032, phase: 0 },
        { x: W * 0.84, y: H * 0.76, r: 320, hue: 170, sat: 58, lig: 58, speed: 0.00026, phase: 1.2 },
        { x: W * 0.70, y: H * 0.12, r: 240, hue: 18, sat: 78, lig: 64, speed: 0.00036, phase: 2.4 },
        { x: W * 0.26, y: H * 0.88, r: 280, hue: 46, sat: 80, lig: 66, speed: 0.00030, phase: 0.8 }
      ];
    }

    function makeParticles() {
      const arr = [];

      for (let i = 0; i < 32; i++) {
        arr.push({
          x: Math.random() * W,
          y: Math.random() * H,
          r: Math.random() * 2.4 + 0.7,
          vx: (Math.random() - 0.5) * 0.42,
          vy: -(Math.random() * 0.42 + 0.14),
          alpha: Math.random() * 0.32 + 0.12,
          hue: 34 + Math.random() * 28
        });
      }

      return arr;
    }

    function drawWaves(t) {
      for (let layer = 0; layer < 4; layer++) {
        ctx.beginPath();

        const yBase = H * (0.32 + layer * 0.12);
        const amp = 20 + layer * 6;
        const freq = 0.0065 - layer * 0.0004;
        const speed = t * (0.00045 + layer * 0.00008);

        ctx.moveTo(0, yBase);

        for (let x = 0; x <= W; x += 8) {
          const y =
            yBase +
            Math.sin(x * freq + speed) * amp +
            Math.cos(x * freq * 0.65 - speed * 0.9) * (amp * 0.38);

          ctx.lineTo(x, y);
        }

        ctx.strokeStyle = `rgba(148,95,12,${0.065 - layer * 0.008})`;
        ctx.lineWidth = layer === 0 ? 1.4 : 1;
        ctx.stroke();
      }
    }

    function drawDots(t) {
      const gap = 82;
      const pulse = (Math.sin(t * 0.0014) + 1) * 0.025;
      const cx = W / 2;
      const cy = H / 2;

      for (let x = gap / 2; x < W; x += gap) {
        for (let y = gap / 2; y < H; y += gap) {
          const dist = Math.hypot(x - cx, y - cy);
          const maxDist = Math.hypot(cx, cy);
          const alpha = Math.max(0, 1 - dist / maxDist) * 0.13 + pulse;

          ctx.beginPath();
          ctx.arc(x, y, 1.25, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(150,95,10,${alpha})`;
          ctx.fill();
        }
      }
    }

    function drawRoundRect(x, y, width, height, radius) {
      if (typeof ctx.roundRect === 'function') {
        ctx.roundRect(x, y, width, height, radius);
        return;
      }

      ctx.moveTo(x + radius, y);
      ctx.lineTo(x + width - radius, y);
      ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
      ctx.lineTo(x + width, y + height - radius);
      ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
      ctx.lineTo(x + radius, y + height);
      ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
      ctx.lineTo(x, y + radius);
      ctx.quadraticCurveTo(x, y, x + radius, y);
    }

    function drawBooks(t) {
      const books = [
        { x: W * 0.09, y: H * 0.72, w: 104, h: 146, rot: -0.16 },
        { x: W * 0.84, y: H * 0.17, w: 80, h: 116, rot: 0.18 },
        { x: W * 0.76, y: H * 0.66, w: 66, h: 98, rot: -0.08 }
      ];

      books.forEach((book, index) => {
        const bob = Math.sin(t * 0.0008 + index) * 6;

        ctx.save();
        ctx.translate(book.x, book.y + bob);
        ctx.rotate(book.rot);

        ctx.fillStyle = 'rgba(255,250,238,.22)';
        ctx.strokeStyle = 'rgba(150,95,10,.18)';
        ctx.lineWidth = 1;

        ctx.beginPath();
        drawRoundRect(-book.w / 2, -book.h / 2, book.w, book.h, 12);
        ctx.fill();
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(-book.w / 2 + 18, -book.h / 2);
        ctx.lineTo(-book.w / 2 + 18, book.h / 2);
        ctx.strokeStyle = 'rgba(150,95,10,.22)';
        ctx.stroke();

        ctx.restore();
      });
    }

    function draw(ts) {
      if (ts - lastFrame < 33) {
        requestAnimationFrame(draw);
        return;
      }

      lastFrame = ts;

      if (!startTime) startTime = ts;
      const t = ts - startTime;

      ctx.fillStyle = '#f7edd8';
      ctx.fillRect(0, 0, W, H);

      orbs.forEach(orb => {
        const angle = t * orb.speed + orb.phase;
        const ox = orb.x + Math.cos(angle) * (W * 0.075);
        const oy = orb.y + Math.sin(angle * 1.2) * (H * 0.065);

        const grad = ctx.createRadialGradient(ox, oy, 0, ox, oy, orb.r);
        grad.addColorStop(0, `hsla(${orb.hue},${orb.sat}%,${orb.lig}%,0.42)`);
        grad.addColorStop(0.45, `hsla(${orb.hue},${orb.sat}%,${orb.lig}%,0.18)`);
        grad.addColorStop(1, `hsla(${orb.hue},${orb.sat}%,${orb.lig}%,0)`);

        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.ellipse(ox, oy, orb.r, orb.r * 0.72, angle * 0.3, 0, Math.PI * 2);
        ctx.fill();
      });

      drawDots(t);
      drawWaves(t);
      drawBooks(t);

      particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;

        if (p.y < -8) {
          p.y = H + 8;
          p.x = Math.random() * W;
        }

        if (p.x < -8) p.x = W + 8;
        if (p.x > W + 8) p.x = -8;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `hsla(${p.hue},78%,48%,${p.alpha})`;
        ctx.fill();
      });

      requestAnimationFrame(draw);
    }

    function initCanvas() {
      resizeCanvas();
      orbs = makeOrbs();
      particles = makeParticles();
      requestAnimationFrame(draw);
    }

    window.addEventListener('resize', () => {
      resizeCanvas();
      orbs = makeOrbs();
    });

    initCanvas();
  })();

// API
  const START_SESSION_URL = "/api/registration/1/start/";
  const REGISTER_STEP_1_URL = "/api/registration/2/validate/username/";
  const REGISTER_STEP_2_URL = "/api/registration/3/validate/email/";
  const REGISTER_TOTP_QR_URL = "/api/registration/4/validate/totp/";
  const REGISTER_STEP_3_URL = "/api/registration/5/confirm/totp/";
  const REGISTER_FINISH_URL = "/api/registration/6/validate/password/";
  const CREATE_USER_ACCOUNT = "/api/registration/7/create/user/";
  const SEND_EMAIL_SMS = "/api/registration/8/activate/email/sms/";

  let registrationAccessToken = null;

  const card = document.getElementById('registerCard');
  const usernameInput = document.getElementById('username');
  const firstNameInput = document.getElementById('firstName');
  const lastNameInput = document.getElementById('lastName');
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');
  const passwordRepeatInput = document.getElementById('passwordRepeat');
  const successState = document.getElementById('successState');
  const qrBox = document.getElementById('qrBox');
  const totpCodeHidden = document.getElementById('totpCodeHidden');

  function getCsrfToken() {
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfInput ? csrfInput.value : '';
  }

  function getErrorMessage(data) {
    if (!data) return 'Xəta baş verdi.';
    if (data.message) return data.message;
    if (data.detail) return data.detail;

    if (typeof data === 'object') {
      const firstKey = Object.keys(data)[0];

      if (firstKey) {
        const firstValue = data[firstKey];

        if (Array.isArray(firstValue)) return firstValue[0];
        if (typeof firstValue === 'string') return firstValue;
      }
    }

    return 'Xəta baş verdi.';
  }

  async function parseResponseData(response) {
    const contentType = response.headers.get('content-type') || '';

    if (contentType.includes('application/json')) {
      return await response.json();
    }

    const text = await response.text();
    const shortText = text.replace(/\s+/g, ' ').trim().slice(0, 120);

    throw new Error(
      `Backend JSON qaytarmadı (${response.status}). Cavab: ${shortText || 'boş cavab'}`
    );
  }

  async function startRegistrationSession() {
    const response = await fetch(START_SESSION_URL, {
      method: 'GET',
    });

    const data = await parseResponseData(response);

    if (!response.ok) {
      throw new Error(getErrorMessage(data));
    }

    registrationAccessToken = data.access_token;

    if (!registrationAccessToken) {
      throw new Error('Registration token backend-dən gəlmədi.');
    }

    return data;
  }

  async function postData(url, payload = {}) {
    if (!registrationAccessToken) {
      throw new Error('Token yoxdur. Səhifəni yeniləyib yenidən yoxlayın.');
    }

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
        'Authorization': `Bearer ${registrationAccessToken}`,
      },
      body: JSON.stringify(payload),
    });

    const data = await parseResponseData(response);

    if (!response.ok || data.ok === false) {
      throw new Error(getErrorMessage(data));
    }

    return data;
  }

  async function getData(url, params = {}) {
    if (!registrationAccessToken) {
      throw new Error('Token yoxdur. Səhifəni yeniləyib yenidən yoxlayın.');
    }

    const query = new URLSearchParams(params).toString();
    const fullUrl = query ? `${url}?${query}` : url;

    const response = await fetch(fullUrl, {
      method: 'GET',
      headers: {
        'X-CSRFToken': getCsrfToken(),
        'Authorization': `Bearer ${registrationAccessToken}`,
      },
    });

    const data = await parseResponseData(response);

    if (!response.ok || data.ok === false) {
      throw new Error(getErrorMessage(data));
    }

    return data;
  }

 function showToast(message, type = 'error') {
  const toastBox = document.getElementById('toastBox');
  const toast = document.createElement('div');

  toast.className = `app-toast ${type === 'success' ? 'success' : ''}`;
  toast.textContent = message;

  toastBox.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 10000);
}

  function setStep(step) {
    card.dataset.step = String(step);
    clearStatuses();

    setTimeout(() => {
      if (step === 0) usernameInput.focus();
      if (step === 1) emailInput.focus();

      if (step === 2) {
        updateTotpActionButton();
        focusCodeGroup('totp');
      }

      if (step === 3) passwordInput.focus();
    }, 260);
  }

  function clearStatuses() {
    document.querySelectorAll('.status').forEach(item => {
      item.textContent = '';
      item.style.color = 'var(--coral)';
    });
  }

  function setButtonLoading(button, isLoading) {
    if (!button) return;

    if (isLoading) {
      if (!button.dataset.originalHtml) {
        button.dataset.originalHtml = button.innerHTML;
      }

      button.disabled = true;
      button.innerHTML = `
        <span class="btn-spinner"></span>
        <span>Yüklənir...</span>
      `;
      return;
    }

    button.disabled = false;

    if (button.dataset.originalHtml) {
      button.innerHTML = button.dataset.originalHtml;
    }
  }

  function validEmail(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  }

  async function submitStep1() {
    const username = usernameInput.value.trim();
    const firstName = firstNameInput.value.trim();
    const lastName = lastNameInput.value.trim();
    const status = document.getElementById('step1Status');
    const button = document.querySelector('[onclick="submitStep1()"]');

    setButtonLoading(button, true);

    try {
      await postData(REGISTER_STEP_1_URL, {
        username,
        first_name: firstName,
        last_name: lastName,
      });

      setStep(1);
    } catch (error) {
      showToast(error.message);
      status.textContent = error.message;
    } finally {
      setButtonLoading(button, false);
    }
  }

  async function submitStep2() {
    const email = emailInput.value.trim();
    const status = document.getElementById('step2Status');
    const button = document.querySelector('[onclick="submitStep2()"]');

    setButtonLoading(button, true);

    try {
      status.style.color = 'var(--ink-muted)';
      status.textContent = 'QR kod hazırlanır...';

      const data = await postData(REGISTER_STEP_2_URL, {
        email,
      });

      const totpData = await getData(REGISTER_TOTP_QR_URL, {
        email,
      });

      renderQrCode(totpData.totp_token_qr_uri);
      showToast(data.message || 'QR kodu uğurla yaradıldı.', 'success');
      setStep(2);
    } catch (error) {
      showToast(error.message);
      status.style.color = 'var(--coral)';
      status.textContent = error.message;
    } finally {
      setButtonLoading(button, false);
    }
  }

  function focusCodeGroup(group) {
    document.querySelector(`[data-code-group="${group}"] .code-input`)?.focus();
  }

  function getCode(group) {
    return [...document.querySelectorAll(`[data-code-group="${group}"] .code-input`)]
      .map(input => input.value)
      .join('');
  }

  function updateTotpActionButton() {
    const button = document.querySelector('[onclick="submitStep3()"]');

    if (!button || button.disabled) return;

    const code = getCode('totp');

    button.innerHTML = code
      ? 'Kodu təsdiqlə <i class="bi bi-check2"></i>'
      : 'Keç <i class="bi bi-arrow-right"></i>';
  }

  async function submitStep3() {
    const code = getCode('totp');
    const status = document.getElementById('step3Status');
    const button = document.querySelector('[onclick="submitStep3()"]');

    if (!code) {
      totpCodeHidden.value = '';
      setStep(3);
      return;
    }

    if (code.length !== 6) {
      status.textContent = '6 rəqəmli kodu tam daxil edin.';
      return;
    }

    setButtonLoading(button, true);

    try {
      await postData(REGISTER_STEP_3_URL, {
        totp_code: code,
      });

      totpCodeHidden.value = code;
      status.style.color = 'var(--teal)';
      status.textContent = 'TOTP kodu təsdiqləndi.';
      setTimeout(() => setStep(3), 240);
    } catch (error) {
      showToast(error.message);
      status.textContent = error.message;
    } finally {
      setButtonLoading(button, false);
    }
  }

  async function submitFinish() {
    const password = passwordInput.value;
    const passwordRepeat = passwordRepeatInput.value;
    const status = document.getElementById('step4Status');
    const button = document.querySelector('[onclick="submitFinish()"]');

    setButtonLoading(button, true);

    try {
      const passwordData = await postData(REGISTER_FINISH_URL, {
        password,
        repeat_password: passwordRepeat,
      });

      if (passwordData.password_confirmed !== true) {
        throw new Error(passwordData.message || 'Parol təsdiqlənmədi.');
      }

      const createUserData = await postData(CREATE_USER_ACCOUNT, {});

      card.style.display = 'none';
      successState.classList.add('show');
      showToast(createUserData.message || passwordData.message || 'Qeydiyyat tamamlandı.', 'success');

      postData(SEND_EMAIL_SMS, {}).catch(error => {
        console.error(error);
        showToast(error.message);
      });
    } catch (error) {
      showToast(error.message);
      status.textContent = error.message;
    } finally {
      setButtonLoading(button, false);
    }
  }

  function renderQrCode(otpAuthUrl) {
    if (!otpAuthUrl) {
      throw new Error('Backend totp_token_qr_uri qaytarmadı.');
    }

    qrBox.innerHTML = '';

    if (typeof QRCode === 'undefined') {
      throw new Error('QR kitabxanası yüklənmədi.');
    }

    new QRCode(qrBox, {
      text: otpAuthUrl,
      width: 188,
      height: 188,
    });
  }

  document.querySelectorAll('.code-row').forEach(row => {
    const inputs = [...row.querySelectorAll('.code-input')];

    inputs.forEach((input, index) => {
      input.addEventListener('input', () => {
        input.value = input.value.replace(/\D/g, '').slice(0, 1);

        if (input.value && inputs[index + 1]) {
          inputs[index + 1].focus();
        }

        if (row.dataset.codeGroup === 'totp') {
          updateTotpActionButton();
        }
      });

      input.addEventListener('keydown', event => {
        if (event.key === 'Backspace' && !input.value && inputs[index - 1]) {
          inputs[index - 1].focus();
        }

        if (row.dataset.codeGroup === 'totp') {
          setTimeout(updateTotpActionButton, 0);
        }
      });

      input.addEventListener('paste', event => {
        event.preventDefault();

        const pasted = event.clipboardData
          .getData('text')
          .replace(/\D/g, '')
          .slice(0, 6);

        pasted.split('').forEach((char, i) => {
          if (inputs[i]) inputs[i].value = char;
        });

        inputs[Math.min(pasted.length, inputs.length - 1)]?.focus();

        if (row.dataset.codeGroup === 'totp') {
          updateTotpActionButton();
        }
      });
    });
  });

  document.addEventListener('DOMContentLoaded', async () => {
    try {
      await startRegistrationSession();
      updateTotpActionButton();
      usernameInput.focus();
    } catch (error) {
      showToast(error.message);
    }
  });
