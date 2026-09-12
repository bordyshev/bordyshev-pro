from pathlib import Path

p = Path("index.html")
s = p.read_text(encoding="utf-8")
if 'id="exitOffer"' in s:
    raise SystemExit("Exit offer already present")

css = r'''.exit-offer{position:fixed;inset:0;z-index:1000;display:none;align-items:center;justify-content:center;padding:20px;background:rgba(0,0,0,.76);backdrop-filter:blur(6px)}.exit-offer.open{display:flex}.exit-box{width:min(560px,100%);background:#fff;color:var(--ink);border:1px solid rgba(255,255,255,.16);box-shadow:0 30px 90px rgba(0,0,0,.45);padding:34px;position:relative;text-align:left}.exit-close{position:absolute;right:14px;top:12px;width:38px;height:38px;border:0;background:#f0efeb;color:#333;font-size:1.45rem;line-height:1;cursor:pointer}.exit-kicker{font-size:.75rem;font-weight:800;text-transform:uppercase;letter-spacing:.12em;color:var(--red);margin-bottom:10px}.exit-box h2{font-family:var(--fh);font-size:clamp(2rem,6vw,3.4rem);line-height:1;text-transform:uppercase;margin:0 0 14px}.exit-box p{margin:0 0 18px;color:#56585d;font-size:.95rem}.exit-benefits{display:grid;gap:8px;margin:0 0 22px;padding:0;list-style:none}.exit-benefits li{position:relative;padding-left:22px;font-size:.88rem}.exit-benefits li:before{content:"✓";position:absolute;left:0;color:var(--good);font-weight:900}.exit-deadline{display:flex;justify-content:space-between;gap:16px;align-items:center;padding:13px 15px;background:#f7eeee;border-left:3px solid var(--red);margin-bottom:18px}.exit-deadline strong{font-size:.86rem}.exit-count{font-family:var(--fh);font-size:1.35rem;color:var(--red);white-space:nowrap}.exit-cta{width:100%;min-height:58px;font-size:1rem}.exit-skip{display:block;margin:12px auto 0;border:0;background:none;color:#777;text-decoration:underline;cursor:pointer;font-size:.78rem}@media(max-width:680px){.exit-box{padding:28px 20px 22px}.exit-deadline{align-items:flex-start;flex-direction:column;gap:6px}.exit-cta{min-height:56px}}'''

modal = r'''<div class="exit-offer" id="exitOffer" role="dialog" aria-modal="true" aria-labelledby="exitOfferTitle" aria-hidden="true">
  <div class="exit-box">
    <button class="exit-close" id="exitOfferClose" aria-label="Закрыть">×</button>
    <div class="exit-kicker">Перед тем как уйти</div>
    <h2 id="exitOfferTitle">Получите бесплатную консультацию</h2>
    <p>Разберу вашу задачу по сайту, SEO, CRM или автоматизации и подскажу, с чего лучше начать без лишних работ.</p>
    <ul class="exit-benefits"><li>Короткий разбор вашей текущей ситуации</li><li>2–3 конкретные идеи без обязательства заказывать проект</li><li>Скидка на первый этап работ, если напишете сегодня</li></ul>
    <div class="exit-deadline"><strong>Предложение действует до конца дня</strong><span class="exit-count" id="exitOfferCountdown">до 23:59</span></div>
    <a class="btn primary exit-cta" href="https://t.me/bordyshev_official?text=Здравствуйте%2C%20хочу%20бесплатную%20консультацию%20и%20скидку%20до%20конца%20дня" target="_blank" rel="noopener">Получить бесплатную консультацию →</a>
    <button class="exit-skip" id="exitOfferSkip">Продолжить просмотр сайта</button>
  </div>
</div>'''

js = r'''<script>
(() => {
  const modal = document.getElementById('exitOffer');
  const closeBtn = document.getElementById('exitOfferClose');
  const skipBtn = document.getElementById('exitOfferSkip');
  const countdown = document.getElementById('exitOfferCountdown');
  if (!modal) return;
  let shown = sessionStorage.getItem('exitOfferShown') === '1';
  const openOffer = () => {
    if (shown) return;
    shown = true;
    sessionStorage.setItem('exitOfferShown','1');
    modal.classList.add('open');
    modal.setAttribute('aria-hidden','false');
    document.body.style.overflow = 'hidden';
  };
  const closeOffer = () => {
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden','true');
    document.body.style.overflow = '';
  };
  closeBtn?.addEventListener('click', closeOffer);
  skipBtn?.addEventListener('click', closeOffer);
  modal.addEventListener('click', e => { if (e.target === modal) closeOffer(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeOffer(); });
  document.addEventListener('mouseout', e => {
    if (e.relatedTarget === null && e.clientY <= 12) openOffer();
  });
  const updateCountdown = () => {
    if (!countdown) return;
    const now = new Date();
    const end = new Date();
    end.setHours(23,59,59,999);
    let diff = Math.max(0, end - now);
    const h = Math.floor(diff / 3600000);
    diff -= h * 3600000;
    const m = Math.floor(diff / 60000);
    diff -= m * 60000;
    const sec = Math.floor(diff / 1000);
    countdown.textContent = `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(sec).padStart(2,'0')}`;
  };
  updateCountdown();
  setInterval(updateCountdown, 1000);
})();
</script>'''

if "  </style>" not in s:
    raise SystemExit("style marker missing")
if '<a id="floatingAudit"' not in s:
    raise SystemExit("floating audit marker missing")
if "</body>" not in s:
    raise SystemExit("body marker missing")

s = s.replace("  </style>", "    " + css + "\n  </style>", 1)
s = s.replace('<a id="floatingAudit"', modal + '\n<a id="floatingAudit"', 1)
s = s.replace("</body>", js + "\n</body>", 1)
p.write_text(s, encoding="utf-8")
