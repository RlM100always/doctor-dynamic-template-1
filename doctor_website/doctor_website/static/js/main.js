'use strict';

document.addEventListener('DOMContentLoaded', () => {
  initBurger();
  initMobileLinks();
  initSmoothScroll();
  initActiveNav();
  initScrollHeader();
  initBackToTop();
  initFAQ();
  initCounters();
  initScrollReveal();
  initRatingBars();
  initAppointmentForm();
  initContactForm();
  initBlogModal();
});

/* ─── 1. BURGER ─── */
function initBurger() {
  const burger = document.getElementById('burger');
  const nav    = document.getElementById('mobileNav');
  if (!burger || !nav) return;

  burger.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    burger.classList.toggle('open', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });

  document.addEventListener('click', (e) => {
    const header = document.getElementById('header');
    if (nav.classList.contains('open') && header && !header.contains(e.target)) {
      nav.classList.remove('open');
      burger.classList.remove('open');
      document.body.style.overflow = '';
    }
  });
}

function initMobileLinks() {
  document.querySelectorAll('.mob-link').forEach(link => {
    link.addEventListener('click', () => {
      const nav    = document.getElementById('mobileNav');
      const burger = document.getElementById('burger');
      if (nav)    nav.classList.remove('open');
      if (burger) burger.classList.remove('open');
      document.body.style.overflow = '';
    });
  });
}

/* ─── 2. SMOOTH SCROLL ─── */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const id = a.getAttribute('href');
      if (id === '#') return;
      const el = document.querySelector(id);
      if (!el) return;
      e.preventDefault();
      const headerH = document.getElementById('header')?.offsetHeight || 80;
      window.scrollTo({ top: el.getBoundingClientRect().top + scrollY - headerH - 8, behavior: 'smooth' });
    });
  });
}

/* ─── 3. ACTIVE NAV ─── */
function initActiveNav() {
  const sections = document.querySelectorAll('section[id]');
  const links    = document.querySelectorAll('.nav__link');
  if (!sections.length || !links.length) return;

  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const id = e.target.id;
        links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === `#${id}`));
      }
    });
  }, { rootMargin: '-40% 0px -55% 0px' });

  sections.forEach(s => io.observe(s));
}

/* ─── 4. SCROLL HEADER ─── */
function initScrollHeader() {
  const header = document.getElementById('header');
  if (!header) return;
  window.addEventListener('scroll', () => {
    header.classList.toggle('scrolled', scrollY > 50);
  }, { passive: true });
}

/* ─── 5. BACK TO TOP ─── */
function initBackToTop() {
  const btn = document.getElementById('btt');
  if (!btn) return;
  window.addEventListener('scroll', () => btn.classList.toggle('visible', scrollY > 400), { passive: true });
  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

/* ─── 6. FAQ ACCORDION ─── */
function initFAQ() {
  const items = document.querySelectorAll('.faq-item');
  items.forEach(item => {
    const btn = item.querySelector('.faq-btn');
    const ans = item.querySelector('.faq-ans');
    if (!btn || !ans) return;

    btn.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');
      // close all
      items.forEach(i => {
        i.classList.remove('open');
        const a = i.querySelector('.faq-ans');
        if (a) a.style.maxHeight = null;
        const ico = i.querySelector('.faq-icon i');
        if (ico) { ico.classList.remove('fa-minus'); ico.classList.add('fa-plus'); }
      });
      if (!isOpen) {
        item.classList.add('open');
        ans.style.maxHeight = ans.scrollHeight + 'px';
        const ico = btn.querySelector('.faq-icon i');
        if (ico) { ico.classList.remove('fa-plus'); ico.classList.add('fa-minus'); }
      }
    });
  });

  // Open first by default
  if (items[0]) {
    items[0].classList.add('open');
    const a = items[0].querySelector('.faq-ans');
    if (a) a.style.maxHeight = a.scrollHeight + 'px';
    const ico = items[0].querySelector('.faq-icon i');
    if (ico) { ico.classList.remove('fa-plus'); ico.classList.add('fa-minus'); }
  }
}

/* ─── 7. COUNTERS ─── */
function initCounters() {
  const counters = document.querySelectorAll('[data-target]');
  if (!counters.length) return;

  const countUp = el => {
    const target = parseInt(el.getAttribute('data-target'), 10);
    const step   = Math.max(1, Math.ceil(target / (2000 / 16)));
    let cur = 0;
    const t = setInterval(() => {
      cur = Math.min(cur + step, target);
      el.textContent = cur.toLocaleString('bn-BD');
      if (cur >= target) clearInterval(t);
    }, 16);
  };

  const io = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { countUp(e.target); io.unobserve(e.target); } });
  }, { threshold: 0.4 });

  counters.forEach(c => { c.textContent = '০'; io.observe(c); });
}

/* ─── 8. SCROLL REVEAL ─── */
function initScrollReveal() {
  const targets = document.querySelectorAll('.reveal');
  const io = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const siblings = Array.from(entry.target.parentNode.children);
        const idx = siblings.indexOf(entry.target);
        entry.target.style.transitionDelay = `${Math.min(idx * 60, 360)}ms`;
        entry.target.classList.add('visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  targets.forEach(t => io.observe(t));
}

/* ─── 9. RATING BARS ─── */
function initRatingBars() {
  const fills = document.querySelectorAll('.rbar__fill');
  if (!fills.length) return;

  fills.forEach(el => {
    const w = el.getAttribute('data-width') || el.style.width;
    el.style.width = '0';
    el.dataset.w = w;
  });

  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        setTimeout(() => { e.target.style.width = e.target.dataset.w; }, 200);
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.5 });

  fills.forEach(el => io.observe(el));
}

/* ─── 10. APPOINTMENT FORM ─── */
function initAppointmentForm() {
  const form     = document.getElementById('apptForm');
  const modal    = document.getElementById('successModal');
  const closeBtn = document.getElementById('closeModalBtn');
  if (!form) return;

  if (closeBtn) closeBtn.addEventListener('click', () => modal.classList.remove('show'));
  if (modal)    modal.addEventListener('click', e => { if (e.target === modal) modal.classList.remove('show'); });

  form.addEventListener('submit', e => {
    e.preventDefault();
    let valid = true;

    const fields = [
      { id: 'aName',  errId: 'aNameErr',  msg: 'নাম লিখুন।' },
      { id: 'aPhone', errId: 'aPhoneErr', msg: 'সঠিক মোবাইল নম্বর দিন।', pattern: /^01[3-9]\d{8}$/ },
      { id: 'aDate',  errId: 'aDateErr',  msg: 'তারিখ নির্বাচন করুন।' },
      { id: 'aTime',  errId: 'aTimeErr',  msg: 'সময় নির্বাচন করুন।' }
    ];

    fields.forEach(f => {
      const inp = document.getElementById(f.id);
      const err = document.getElementById(f.errId);
      if (!inp || !err) return;
      err.textContent = '';
      inp.style.borderColor = '';
      const val = inp.value.trim();
      if (!val || (f.pattern && !f.pattern.test(val))) {
        err.textContent = f.msg;
        inp.style.borderColor = '#e53e3e';
        valid = false;
      }
    });

    if (!valid) return;

    const data = {
      name:    document.getElementById('aName').value,
      phone:   document.getElementById('aPhone').value,
      date:    document.getElementById('aDate').value,
      time:    document.getElementById('aTime').value,
      problem: document.getElementById('aNote').value
    };

    const btn = form.querySelector('button[type="submit"]');
    if (btn) btn.disabled = true;

    fetch('https://script.google.com/macros/s/AKfycbzYJjGfQvrtR6mD86p32LovCA295ZYl0NMoeGrHEzg916vRuMaV5xzMhQ_6Oena2dyDCA/exec', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      redirect: 'follow'
    })
    .then(r => r.json())
    .then(res => {
      if (res.result === 'success') { modal.classList.add('show'); form.reset(); }
      else throw new Error(res.error);
    })
    .catch(err => {
      console.error(err);
      alert('ডাটা পাঠাতে সমস্যা হয়েছে। ইন্টারনেট কানেকশন চেক করুন।');
    })
    .finally(() => { if (btn) btn.disabled = false; });
  });
}

/* ─── 11. CONTACT FORM ─── */
function initContactForm() {
  const form     = document.getElementById('contactForm');
  const modal    = document.getElementById('contactSuccessModal');
  const closeBtn = document.getElementById('closeContactModal');
  if (!form) return;

  if (closeBtn) closeBtn.addEventListener('click', () => modal.classList.remove('show'));
  if (modal)    modal.addEventListener('click', e => { if (e.target === modal) modal.classList.remove('show'); });

  form.addEventListener('submit', e => {
    e.preventDefault();
    let valid = true;

    ['cName', 'cPhone', 'cMsg'].forEach(id => {
      const el = document.getElementById(id);
      if (el && !el.value.trim()) { el.style.borderColor = '#e53e3e'; valid = false; }
      else if (el) el.style.borderColor = '';
    });

    if (!valid) return;

    const data = {
      name:    document.getElementById('cName').value,
      phone:   document.getElementById('cPhone').value,
      email:   document.getElementById('cEmail').value,
      message: document.getElementById('cMsg').value
    };

    const btn = form.querySelector('button[type="submit"]');
    if (btn) btn.disabled = true;

    fetch('https://script.google.com/macros/s/AKfycbxwIzFWC8Asfk978mMEqNimXS6lATM5XD5oAImK_5lwiKbjBO9irHwswLezTgSPanO-/exec', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { 'Content-Type': 'text/plain;charset=utf-8' }
    })
    .then(r => r.json())
    .then(res => {
      if (res.result === 'success') { modal.classList.add('show'); form.reset(); }
      else throw new Error(res.error || 'Error');
    })
    .catch(err => { console.error(err); alert('ডাটা পাঠাতে সমস্যা হয়েছে।'); })
    .finally(() => { if (btn) btn.disabled = false; });
  });
}

/* ─── 12. BLOG MODAL ─── */
const blogContent = {
  blog1: `
    <h2>গর্ভাবস্থায় কী খাবেন, কী এড়িয়ে চলবেন?</h2>
    <p>সুষম পুষ্টি, নিরাপদ ব্যায়াম এবং মানসিক স্বাস্থ্য — গর্ভকালীন সময়ে এই তিনটি বিষয়ে সঠিক জ্ঞান থাকা অত্যন্ত জরুরি।</p>

    <h3>✅ যা খাবেন</h3>
    <ul>
      <li>সবজি ও স্যালাড: ব্রোকলি, পালং শাক, গাজর</li>
      <li>ডাল ও লেগিউম: ছোলা, মুগ ডাল</li>
      <li>ফাইবার সমৃদ্ধ শস্য: ওটস, চিড়া, লাল চাল</li>
      <li>প্রোটিন: মাছ, মুরগি, ডিম ও দুধ</li>
      <li>ফলমূল: আম, কলা, পেয়ারা, আপেল</li>
    </ul>

    <h3>❌ যা এড়িয়ে চলবেন</h3>
    <ul>
      <li>কাঁচা বা আধা সেদ্ধ মাংস ও মাছ</li>
      <li>অতিরিক্ত চিনি, ক্যাফেইন ও প্রসেসড খাবার</li>
      <li>পাস্তুরাইজড নয় এমন দুধ বা পনির</li>
      <li>অ্যালকোহল ও ধূমপান সম্পূর্ণ নিষেধ</li>
    </ul>

    <h3>ব্যায়াম ও বিশ্রাম</h3>
    <p>প্রতিদিন হালকা হাঁটাহাঁটি, যোগব্যায়াম এবং পর্যাপ্ত ঘুম মা ও শিশু উভয়ের জন্য উপকারী। ভারী ব্যায়াম বা পড়ে যাওয়ার ঝুঁকি আছে এমন কাজ এড়িয়ে চলুন।</p>

    <h3>মানসিক স্বাস্থ্য</h3>
    <p>গর্ভাবস্থায় মানসিক চাপ কম রাখুন। পরিবারের সাথে সময় কাটান, পছন্দের বই পড়ুন এবং ডাক্তারের সাথে নিয়মিত পরামর্শ রাখুন।</p>
  `,
  blog2: `
    <h2>পিসিওএস কী এবং কীভাবে নিয়ন্ত্রণ করবেন?</h2>
    <p>পলিসিস্টিক ওভারি সিনড্রোম (PCOS) একটি হরমোনজনিত সমস্যা যা প্রজনন বয়সের নারীদের মধ্যে অত্যন্ত সাধারণ।</p>

    <h3>লক্ষণসমূহ</h3>
    <ul>
      <li>অনিয়মিত বা বন্ধ মাসিক</li>
      <li>অতিরিক্ত ওজন বৃদ্ধি</li>
      <li>মুখে ও শরীরে অতিরিক্ত লোম</li>
      <li>ত্বকে ব্রণ</li>
      <li>গর্ভধারণে সমস্যা</li>
    </ul>

    <h3>কারণ</h3>
    <p>সঠিক কারণ অজানা, তবে ইনসুলিন রেজিস্ট্যান্স, হরমোন ভারসাম্যহীনতা এবং বংশগত কারণ ভূমিকা পালন করে।</p>

    <h3>চিকিৎসা ও ব্যবস্থাপনা</h3>
    <ul>
      <li>জীবনযাত্রার পরিবর্তন: নিয়মিত ব্যায়াম ও স্বাস্থ্যকর খাদ্য</li>
      <li>হরমোন থেরাপি: ডাক্তারের পরামর্শ অনুযায়ী</li>
      <li>মেটফর্মিন: ইনসুলিন নিয়ন্ত্রণে</li>
      <li>নিয়মিত ফলোআপ ও পরীক্ষা-নিরীক্ষা</li>
    </ul>
    <p>পিসিওএস নিয়ন্ত্রণে রাখলে স্বাভাবিক গর্ভধারণ সম্ভব। বিস্তারিত পরামর্শের জন্য ডাঃ সানজিদার সাথে যোগাযোগ করুন।</p>
  `,
  blog3: `
    <h2>প্রিক্ল্যাম্পসিয়া: নীরব বিপদ চেনার উপায়</h2>
    <p>প্রিক্ল্যাম্পসিয়া হলো গর্ভাবস্থায় উচ্চ রক্তচাপ ও প্রস্রাবে প্রোটিন নির্গমনের একটি গুরুতর জটিলতা, যা সাধারণত ২০ সপ্তাহের পরে দেখা যায়।</p>

    <h3>সতর্কসংকেত</h3>
    <ul>
      <li>হঠাৎ রক্তচাপ বৃদ্ধি (140/90 বা তার বেশি)</li>
      <li>মাথাব্যথা ও দৃষ্টি ঝাপসা হওয়া</li>
      <li>পেটের উপরিভাগে তীব্র ব্যথা</li>
      <li>হাত-পা ও মুখ ফোলা</li>
      <li>প্রস্রাব কমে যাওয়া</li>
    </ul>

    <h3>ঝুঁকি কমানোর উপায়</h3>
    <ul>
      <li>নিয়মিত প্রসবপূর্ব চেকআপ করান</li>
      <li>রক্তচাপ নিয়মিত পরিমাপ করুন</li>
      <li>লবণ ও চর্বিযুক্ত খাবার কম খান</li>
      <li>পর্যাপ্ত বিশ্রাম নিন</li>
    </ul>

    <h3>কখন ডাক্তার দেখাবেন?</h3>
    <p>উপরের কোনো লক্ষণ দেখা দিলে সাথে সাথে ডাক্তারের সাথে যোগাযোগ করুন। সময়মতো চিকিৎসায় মা ও শিশু উভয়কেই সুরক্ষিত রাখা সম্ভব।</p>
  `
};

function initBlogModal() {
  const modal     = document.getElementById('blog-modal');
  const body      = document.getElementById('blog-modal-body');
  const closeBtn  = document.getElementById('blogModalClose');

  if (!modal) return;

  // Open on blog card click
  document.querySelectorAll('.blog-card').forEach(card => {
    card.addEventListener('click', () => {
      const id = card.getAttribute('data-content');
      if (!id || !blogContent[id]) return;
      body.innerHTML = blogContent[id];
      modal.style.display = 'flex';
      document.body.style.overflow = 'hidden';
    });
  });

  // Close button
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      modal.style.display = 'none';
      document.body.style.overflow = '';
    });
  }

  // Click outside to close
  modal.addEventListener('click', e => {
    if (e.target === modal) {
      modal.style.display = 'none';
      document.body.style.overflow = '';
    }
  });

  // ESC to close
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && modal.style.display === 'flex') {
      modal.style.display = 'none';
      document.body.style.overflow = '';
    }
  });
}