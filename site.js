// Everything is pre-rendered into index.html by build.py, so crawlers that do not run
// JavaScript still see every entry and abstract. This script only adds behaviour:
// publication filters, abstract toggles, draggable stickers, and the active nav link.
document.addEventListener('DOMContentLoaded', () => {
    // --- publication filters ------------------------------------------------
    const pubs = Array.from(document.querySelectorAll('.pub'));
    const years = Array.from(document.querySelectorAll('.pub-year'));
    const filters = Array.from(document.querySelectorAll('.filter'));
    const empty = document.querySelector('.pub-empty');

    function select(filter) {
        let visible = 0;
        pubs.forEach(pub => {
            const show = filter === 'all' || pub.dataset.tags.split(' ').includes(filter);
            pub.hidden = !show;
            if (show) visible++;
        });
        years.forEach(year => {
            year.hidden = !year.querySelector('.pub:not([hidden])');
        });
        if (empty) empty.hidden = visible > 0;
        filters.forEach(btn => btn.setAttribute('aria-pressed', String(btn.dataset.filter === filter)));
    }

    filters.forEach(btn => btn.addEventListener('click', () => select(btn.dataset.filter)));

    // --- abstracts ----------------------------------------------------------
    document.querySelectorAll('.abstract-toggle').forEach(btn => {
        const abstract = document.getElementById(btn.getAttribute('aria-controls'));
        btn.addEventListener('click', () => {
            const open = btn.getAttribute('aria-expanded') !== 'true';
            btn.setAttribute('aria-expanded', String(open));
            abstract.classList.toggle('is-open', open);
        });
    });

    // A link to #some-paper (e.g. from "What I build") should never land on a
    // paper hidden by the current filter.
    window.addEventListener('hashchange', () => {
        const target = document.getElementById(location.hash.slice(1));
        if (target && target.matches('.pub[hidden]')) {
            select('all');
            target.scrollIntoView();
        }
    });

    // --- assembly line in the hero ------------------------------------------
    // The machine swallows a few tokens, presses, and pushes the next logo onto the
    // belt while the meter shows params going up and loss going down. Hovering
    // pauses the line so a logo can be clicked. Reduced motion keeps the static row.
    const factory = document.querySelector('.factory');
    if (factory && !matchMedia('(prefers-reduced-motion: reduce)').matches) runFactory(factory);

    // --- active section in the navigation -----------------------------------
    const navLinks = new Map(
        Array.from(document.querySelectorAll('[data-nav]')).map(a => [a.dataset.nav, a])
    );
    const sections = Array.from(navLinks.keys())
        .map(id => document.getElementById(id))
        .filter(Boolean);
    if (!sections.length || !('IntersectionObserver' in window)) return;

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            navLinks.forEach((a, id) => {
                const active = id === entry.target.id;
                a.classList.toggle('is-active', active);
                if (active) a.setAttribute('aria-current', 'true');
                else a.removeAttribute('aria-current');
            });
        });
    }, { rootMargin: '-35% 0px -60% 0px' });
    sections.forEach(section => observer.observe(section));
});

function runFactory(root) {
    const SPEED = 48;    // px/s; matches belt-run in style.css (12px every 0.25s)
    const CYCLE = 5000;  // ms between two logos
    const machine = root.querySelector('.factory-machine');
    const box = root.querySelector('.factory-items');
    const templates = Array.from(box.children);
    const tokens = JSON.parse(root.dataset.tokens || '[]');
    const paramsEl = root.querySelector('[data-params]');
    const lossEl = root.querySelector('[data-loss]');
    const spark = root.querySelector('.factory-spark polyline');

    box.replaceChildren();
    root.classList.add('is-live');

    let paused = false;
    let visible = true;
    let timer = null;
    let bag = [];
    let params = 1;
    let losses = [];
    const anims = new Set();

    const mpx = () => parseFloat(getComputedStyle(root).getPropertyValue('--mpx'));
    const random = list => list[Math.floor(Math.random() * list.length)];

    // Run a Web Animation on a temporary node and remove the node when it ends.
    function play(node, keyframes, options) {
        const anim = node.animate(keyframes, options);
        anims.add(anim);
        if (paused) anim.pause();
        const done = () => { anims.delete(anim); node.remove(); };
        anim.finished.then(done, done);
        return anim;
    }

    function dropTokens() {
        const m = mpx();
        const x = machine.offsetLeft + 9 * m;  // hopper mouth
        const y = machine.offsetTop + 3 * m;
        for (let i = 0; i < 3; i++) {
            const t = document.createElement('span');
            t.className = 'factory-token';
            t.textContent = random(tokens);
            root.append(t);
            const cx = x - t.offsetWidth / 2;
            const from = cx + (Math.random() * 8 - 4) * m;
            play(t, [
                { transform: `translate(${from}px, -18px) rotate(${Math.random() * 60 - 30}deg)`, opacity: 0 },
                { opacity: 1, offset: 0.25 },
                { transform: `translate(${cx}px, ${y}px) rotate(0deg) scale(1)`, opacity: 1, offset: 0.85 },
                { transform: `translate(${cx}px, ${y + 3 * m}px) rotate(0deg) scale(0.4)`, opacity: 0 },
            ], { duration: 700, delay: i * 140, easing: 'ease-in', fill: 'backwards' });
        }
    }

    function puff() {
        const m = mpx();
        const s = document.createElement('span');
        s.className = 'factory-smoke';
        root.append(s);
        const x = machine.offsetLeft + 19.5 * m - 5;
        const y = machine.offsetTop - 8;
        play(s, [
            { transform: `translate(${x}px, ${y}px) scale(0.4)`, opacity: 0.9 },
            { transform: `translate(${x + 16}px, ${y - 36}px) scale(1.7)`, opacity: 0 },
        ], { duration: 1100, easing: 'ease-out' });
    }

    function press() {
        machine.classList.remove('is-pressing');
        void machine.offsetWidth;  // restart the CSS animation
        machine.classList.add('is-pressing');
        puff();
        setTimeout(puff, 200);
    }

    // Shuffle bag: every logo comes out once before any comes out again, and a new
    // round never starts with the logo that just ended the previous one.
    let last = null;
    function next() {
        if (!bag.length) {
            bag = templates.slice();
            for (let i = bag.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [bag[i], bag[j]] = [bag[j], bag[i]];
            }
            if (bag.length > 1 && bag[bag.length - 1] === last) [bag[0], bag[bag.length - 1]] = [bag[bag.length - 1], bag[0]];
        }
        last = bag.pop();
        return last;
    }

    // Push the next logo out of the chute; `ahead` fast-forwards it (to prefill the belt).
    function output(ahead = 0) {
        const el = next().cloneNode(true);
        el.tabIndex = -1;
        el.setAttribute('aria-hidden', 'true');
        box.append(el);
        const start = machine.offsetLeft + 24 * mpx() - el.offsetWidth;  // tucked behind the chute
        const end = root.clientWidth + 24;
        const anim = play(el, [
            { transform: `translateX(${start}px)` },
            { transform: `translateX(${end}px)` },
        ], { duration: ((end - start) / SPEED) * 1000, easing: 'linear' });
        anim.currentTime = ahead;
        if (!ahead) {
            el.querySelector('svg').animate(
                [{ transform: 'scale(1)' }, { transform: 'scale(1.15, 0.85)' }, { transform: 'scale(1)' }],
                { duration: 350, delay: (el.offsetWidth / SPEED) * 1000, easing: 'ease-out' },
            );
        }
    }

    function meter() {
        params *= 1.7;
        if (params > 5000) {  // out of GPUs: start over
            params = 1;
            losses = [];
            paramsEl.textContent = 'OOM';
            return;
        }
        losses.push(1.7 + 1.5 * Math.exp(-losses.length / 5) + Math.random() * 0.08);
        paramsEl.textContent = params >= 1000 ? `${(params / 1000).toFixed(1)}T` : `${params.toFixed(params < 10 ? 1 : 0)}B`;
        lossEl.textContent = losses[losses.length - 1].toFixed(2);
        const shown = losses.slice(-20);
        const n = Math.max(shown.length - 1, 1);
        spark.setAttribute('points', shown
            .map((l, i) => `${((i / n) * 60).toFixed(1)},${(((3.3 - l) / 1.7) * 20).toFixed(1)}`)
            .join(' '));
    }

    function cycle() {
        timer = null;
        if (paused || !visible) return;
        dropTokens();
        setTimeout(press, 800);
        setTimeout(() => { output(); meter(); }, 950);
        timer = setTimeout(cycle, CYCLE);
    }

    function resume() {
        if (!paused && visible && !timer) timer = setTimeout(cycle, 300);
    }

    root.addEventListener('pointerenter', () => {
        paused = true;
        root.classList.add('is-paused');
        anims.forEach(a => a.pause());
    });
    root.addEventListener('pointerleave', () => {
        paused = false;
        root.classList.remove('is-paused');
        anims.forEach(a => a.play());
        resume();
    });
    new IntersectionObserver(([entry]) => {
        visible = entry.isIntersecting;
        resume();
    }).observe(root);

    // Start with a few logos already on their way.
    for (let k = 2; k >= 1; k--) {
        output(k * CYCLE);
        meter();
    }
}
