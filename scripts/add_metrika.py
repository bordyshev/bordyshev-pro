from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
counter = '108996416'

if f'ym({counter}' in s or 'mc.yandex.ru/metrika/tag.js' in s:
    raise SystemExit('Yandex Metrika already present; aborting to avoid duplicate counter')

metrika = '''
  <!-- Yandex.Metrika counter -->
  <script type="text/javascript">
    (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
    m[i].l=1*new Date();
    for (var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}
    k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
    (window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");
    ym(108996416,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});
  </script>
  <!-- /Yandex.Metrika counter -->
'''
s = s.replace('</head>', metrika + '</head>', 1)

noscript = '<noscript><div><img src="https://mc.yandex.ru/watch/108996416" style="position:absolute;left:-9999px" alt="" /></div></noscript>\n'
s = s.replace('<body>', '<body>\n' + noscript, 1)

s = s.replace(
    '<a class="btn ghost" href="https://t.me/bordyshev_official" target="_blank" rel="noopener">Написать в Telegram</a>',
    '<a id="heroTelegram" class="btn ghost" href="https://t.me/bordyshev_official" target="_blank" rel="noopener">Написать в Telegram</a>',
    1,
)

max_href = 'https://max.ru/u/f9LHodD0cOJBV1T3BpTBwe68VrgL1G6RXTrwWW2RSpDvZWPYYeOesmhELEY'
s = s.replace(
    f'<a href="{max_href}" target="_blank" rel="noopener"><span>MAX</span>',
    f'<a id="contactMax" href="{max_href}" target="_blank" rel="noopener"><span>MAX</span>',
    1,
)

s = s.replace(
    '<a class="btn primary exit-cta" href="https://t.me/bordyshev_official?text=',
    '<a id="exitOfferCta" class="btn primary exit-cta" href="https://t.me/bordyshev_official?text=',
    1,
)

tracking = '''
<script>
(() => {
  const METRIKA_ID = 108996416;
  const goal = (name) => {
    if (typeof window.ym === 'function') {
      window.ym(METRIKA_ID, 'reachGoal', name);
    }
  };

  const clickGoals = [
    ['auditBtn', 'hero_audit'],
    ['floatingAudit', 'hero_audit'],
    ['heroTelegram', 'hero_telegram'],
    ['emailContact', 'contact_email'],
    ['contactMax', 'contact_max'],
    ['exitOfferCta', 'exit_offer']
  ];

  clickGoals.forEach(([id, name]) => {
    document.getElementById(id)?.addEventListener('click', () => goal(name));
  });

  const observedGoals = [
    ['prices', 'view_prices'],
    ['cases', 'view_cases']
  ];

  if ('IntersectionObserver' in window) {
    const fired = new Set();
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting || entry.intersectionRatio < 0.35) return;
        const item = observedGoals.find(([id]) => id === entry.target.id);
        if (!item) return;
        const [, name] = item;
        if (fired.has(name)) return;
        fired.add(name);
        goal(name);
        observer.unobserve(entry.target);
      });
    }, { threshold: [0.35] });

    observedGoals.forEach(([id]) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });
  }
})();
</script>
'''
s = s.replace('</body>', tracking + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
