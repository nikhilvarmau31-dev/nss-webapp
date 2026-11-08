// ─── Flash message auto-close ───────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss flash alerts after 5 seconds
    document.querySelectorAll('.alert').forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(50px)';
            alert.style.transition = 'all 0.4s ease';
            setTimeout(function () { alert.remove(); }, 400);
        }, 5000);
        // Manual close
        const closeBtn = alert.querySelector('.close-alert');
        if (closeBtn) {
            closeBtn.addEventListener('click', function () {
                alert.style.opacity = '0';
                setTimeout(function () { alert.remove(); }, 300);
            });
        }
    });

    // ─── Event filter buttons ─────────────────────────────────
    document.querySelectorAll('.events-filter .filter-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            document.querySelectorAll('.events-filter .filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            const filter = this.dataset.filter;
            document.querySelectorAll('.event-list-card').forEach(function (card) {
                if (filter === 'all' || card.classList.contains(filter)) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // ─── Gallery / News filter buttons ────────────────────────
    document.querySelectorAll('.gallery-filter .filter-btn, .news-filter .filter-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const parentFilter = this.closest('.gallery-filter, .news-filter');
            parentFilter.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            const filter = this.dataset.filter;
            const items = document.querySelectorAll('.gallery-item, .news-full-card');
            items.forEach(function (item) {
                if (filter === 'all' || item.classList.contains(filter)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });

    // ─── Smooth scroll for in-page anchor links ───────────────
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ─── Sticky navbar background change on scroll ────────────
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.5)';
                navbar.style.backdropFilter = 'blur(10px)';
            } else {
                navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.3)';
            }
        });
    }

    // ─── Animate stats counter ────────────────────────────────
    const statNums = document.querySelectorAll('.stat-num[data-count]');
    if (statNums.length) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const target = parseInt(el.dataset.count, 10) || 0;
                    if (target === 0) return;
                    let start = 0;
                    const duration = 1500;
                    const step = Math.ceil(duration / target);
                    const timer = setInterval(function () {
                        start += Math.max(1, Math.ceil(target / 60));
                        if (start >= target) { el.textContent = target; clearInterval(timer); }
                        else { el.textContent = start; }
                    }, step > 50 ? 50 : step);
                    observer.unobserve(el);
                }
            });
        }, { threshold: 0.5 });
        statNums.forEach(function (el) { observer.observe(el); });
    }

    // ─── Form validation feedback ─────────────────────────────
    document.querySelectorAll('form[novalidate]').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const required = form.querySelectorAll('[required]');
            let valid = true;
            required.forEach(function (field) {
                field.style.borderColor = '';
                if (!field.value.trim()) {
                    field.style.borderColor = '#c0392b';
                    valid = false;
                }
            });
            if (!valid) {
                e.preventDefault();
                const first = form.querySelector('[required]:invalid, [required][style*="c0392b"]');
                if (first) first.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    });

    // ─── Animate cards on scroll (Intersection Observer) ─────
    const cards = document.querySelectorAll('.activity-card, .event-card, .news-card, .stat-card, .benefit-card');
    const cardObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                cardObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    cards.forEach(function (card) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        cardObserver.observe(card);
    });
});

// ─── Month name helper (injected via Jinja, but also client-side fallback)
const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
