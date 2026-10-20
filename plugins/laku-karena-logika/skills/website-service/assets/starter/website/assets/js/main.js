/* Venturo.id — small progressive enhancements. Page works fully without JS. */
(function () {
  'use strict';

  // ---- WhatsApp links: a prefilled message per CTA context ----
  // Sales: 0851-2804-3814 · Recruitment (magang & karir): 0851-7418-7053
  var WA_SALES = '6285128043814';
  var WA_MAGANG = '6285174187053';
  // Google Ads conversion for WhatsApp leads: fill in 'AW-16682756931/<label>' from Google Ads › Goals › Conversions.
  var ADS_CONVERSION = '';
  var WA_MESSAGES = {
    general:   'Halo Venturo, saya ingin konsultasi gratis tentang kebutuhan tim developer / proyek software perusahaan saya.',
    squad:     'Halo Venturo, saya ingin cek ketersediaan dedicated squad programmer untuk proyek kami.',
    bulanan:   'Halo Venturo, saya ingin tahu biaya bulanan dedicated programmer, sebagai alternatif merekrut karyawan IT sendiri.',
    longterm:  'Halo Venturo, saya ingin diskusi kerja sama proyek jangka panjang (long term) dengan dedicated squad.',
    shortterm: 'Halo Venturo, saya ingin diskusi kerja sama proyek jangka pendek (short term).',
    managed:   'Halo Venturo, saya ingin tahu lebih lanjut tentang paket Managed Services untuk aplikasi kami.',
    cloud:     'Halo Venturo, saya ingin konsultasi kebutuhan server / Venturo Cloud.',
    poc:       'Halo Venturo, saya tertarik dengan program Free Proof of Concept. Boleh dijelaskan syarat dan jadwalnya?',
    jakarta:   'Halo Venturo, saya dari Jakarta dan butuh tim programmer outsourcing. Boleh konsultasi?',
    ai:        'Halo Venturo, saya ingin konsultasi pembuatan solusi AI untuk bisnis saya.',
    aipoc:     'Halo Venturo, saya ingin mengajukan Free Proof of Concept untuk proyek AI kami.',
    magang:    'Halo Venturo, saya ingin mendaftar program Magang IT / Internship Programmer di Malang.',
    karir:     'Halo Venturo, saya ingin bertanya tentang lowongan kerja programmer / IT di Venturo.',
    malang:    'Halo Venturo, saya mencari software house di Malang dan ingin konsultasi / jadwalkan meeting.',
    aplikasi:  'Halo Venturo, saya ingin konsultasi jasa pembuatan aplikasi / software custom untuk bisnis saya.',
    web:       'Halo Venturo, saya ingin konsultasi jasa pembuatan aplikasi web untuk bisnis saya.',
    android:   'Halo Venturo, saya ingin konsultasi jasa pembuatan aplikasi Android / iOS.',
    website:   'Halo Venturo, saya ingin konsultasi jasa pembuatan website perusahaan.',
    maintenance: 'Halo Venturo, saya ingin konsultasi jasa maintenance aplikasi / website (Managed Services).',
    harga:     'Halo Venturo, saya ingin minta estimasi biaya pembuatan aplikasi.',
    enterprise: 'Halo Venturo, saya ingin menjadwalkan AI assessment untuk program Enterprise AI Transformation di perusahaan kami.'
  };

  document.querySelectorAll('[data-wa]').forEach(function (a) {
    var key = a.getAttribute('data-wa');
    var msg = a.getAttribute('data-wa-text') || WA_MESSAGES[key] || WA_MESSAGES.general;
    var number = (key === 'magang' || key === 'karir') ? WA_MAGANG : WA_SALES;
    a.href = 'https://wa.me/' + number + '?text=' + encodeURIComponent(msg);
    a.target = '_blank';
    a.rel = 'noopener';
    a.addEventListener('click', function () {
      // Conversion tracking hook (works when GA4 / GTM is installed)
      var label = a.getAttribute('data-cta') || 'unknown';
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'generate_lead', { method: 'whatsapp', cta_position: label });
        if (ADS_CONVERSION && number === WA_SALES) window.gtag('event', 'conversion', { send_to: ADS_CONVERSION });
      }
      if (Array.isArray(window.dataLayer)) {
        window.dataLayer.push({ event: 'wa_click', cta_position: label });
      }
    });
  });

  // ---- Sticky header shadow ----
  var header = document.querySelector('.header');
  var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // ---- Mobile nav ----
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  var setNav = function (open) {
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Tutup menu' : 'Buka menu');
  };
  toggle.addEventListener('click', function () { setNav(!nav.classList.contains('is-open')); });
  nav.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { setNav(false); }); });

  // ---- "Layanan" dropdown (hover on desktop via CSS; click/tap + keyboard here) ----
  document.querySelectorAll('.nav__dd').forEach(function (dd) {
    var btn = dd.querySelector('.nav__ddbtn');
    btn.addEventListener('click', function () {
      var open = !dd.classList.contains('is-open');
      dd.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('click', function (e) {
      if (!dd.contains(e.target)) { dd.classList.remove('is-open'); btn.setAttribute('aria-expanded', 'false'); }
    });
  });

  // ---- Simple tabs (curriculum on the internship page) ----
  document.querySelectorAll('[data-tabs]').forEach(function (wrap) {
    var tabs = wrap.querySelectorAll('[role="tab"]');
    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        tabs.forEach(function (t) {
          var on = t === tab;
          t.setAttribute('aria-selected', String(on));
          document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
        });
      });
    });
  });

  // ---- Cost estimator (no prices shown): composes a WhatsApp message ----
  document.querySelectorAll('[data-estimator]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var pick = function (name) {
        return [].map.call(form.querySelectorAll('input[name="' + name + '"]:checked'), function (i) { return i.value; }).join(' + ');
      };
      var msg = 'Halo Venturo, saya ingin estimasi biaya pembuatan aplikasi.\n' +
        '• Platform: ' + (pick('platform') || '-') + '\n' +
        '• Fitur yang dibutuhkan: ' + (((form.querySelector('[name="fitur"]') || {}).value || '').trim() || '-') + '\n' +
        '• Skema: ' + pick('skema');
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'generate_lead', { method: 'whatsapp', cta_position: 'estimator' });
        if (ADS_CONVERSION) window.gtag('event', 'conversion', { send_to: ADS_CONVERSION });
      }
      if (Array.isArray(window.dataLayer)) window.dataLayer.push({ event: 'wa_click', cta_position: 'estimator' });
      window.open('https://wa.me/' + WA_SALES + '?text=' + encodeURIComponent(msg), '_blank', 'noopener');
    });
  });

  // ---- Reveal on scroll ----
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('is-visible'); });
  }

  // ---- Promo dates always follow the current month (e.g. "Oktober 2026", "31 Okt 2026") ----
  var now = new Date();
  var MONTHS = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];
  var MONTHS_SHORT = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];
  var lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
  document.querySelectorAll('[data-month]').forEach(function (el) {
    el.textContent = MONTHS[now.getMonth()] + ' ' + now.getFullYear();
  });
  document.querySelectorAll('[data-month-end]').forEach(function (el) {
    el.textContent = lastDay + ' ' + MONTHS_SHORT[now.getMonth()] + ' ' + now.getFullYear();
  });

  // ---- Footer year ----
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // ---- Lightweight YouTube embed: load the player only after a click (keeps PageSpeed high) ----
  document.querySelectorAll('[data-yt]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var id = btn.getAttribute('data-yt');
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&playsinline=1';
      f.title = btn.getAttribute('aria-label') || 'Video';
      f.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen';
      f.allowFullscreen = true;
      btn.replaceChildren(f);
      btn.style.cursor = 'default';
    }, { once: true });
  });
})();
