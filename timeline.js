// The timeline is pre-rendered into index.html by build.py from data/timeline.json,
// so crawlers that do not run JavaScript still see every entry. This script only
// toggles visibility of those existing nodes.
document.addEventListener('DOMContentLoaded', () => {
    const entries = Array.from(document.querySelectorAll('.timeline-entry'));
    const buttons = Array.from(document.querySelectorAll('.filter-btn'));
    const emptyMsg = document.getElementById('timeline-empty');
    if (!entries.length) return;

    function select(filter) {
        let visible = 0;
        entries.forEach(entry => {
            const tags = (entry.dataset.tags || '').split(' ');
            const show = filter === 'all'
                ? true
                : !tags.includes('news') && tags.includes(filter);
            entry.hidden = !show;
            if (show) visible++;
        });
        if (emptyMsg) emptyMsg.classList.toggle('hidden', visible > 0);

        buttons.forEach(btn => {
            const active = btn.dataset.filter === filter;
            btn.setAttribute('aria-pressed', String(active));
            btn.classList.toggle('bg-blue-600', active);
            btn.classList.toggle('text-white', active);
            btn.classList.toggle('bg-gray-200', !active);
            btn.classList.toggle('text-gray-700', !active);
        });
    }

    buttons.forEach(btn => btn.addEventListener('click', () => select(btn.dataset.filter)));
});
