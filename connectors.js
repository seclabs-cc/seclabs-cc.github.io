document.addEventListener('DOMContentLoaded', () => {
    const heroContent = document.querySelector('.hero-content');
    const titleAccent = document.querySelector('.hero-title .title-accent');
    const subtitleFrame = document.querySelector('.subtitle-frame');
    const initials = Array.from(document.querySelectorAll('.hero-subtitle .subtitle-initial'));

    if (!heroContent || !titleAccent || !subtitleFrame || initials.length !== 3) return;

    const textNode = titleAccent.firstChild;
    if (!textNode) return;

    const svgNS = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(svgNS, 'svg');
    svg.classList.add('rtm-connectors');
    svg.setAttribute('aria-hidden', 'true');
    heroContent.insertBefore(svg, heroContent.firstChild);

    const BOTTOM_CLEARANCE = 18;
    const ROW_STAGGER = [10, 7, 14]; // extra px above the clearance line, per letter (R, T, M)
    const traces = [0, 1, 2].map(() => {
        const trace = document.createElementNS(svgNS, 'path');
        trace.classList.add('connector-trace');
        const flow = document.createElementNS(svgNS, 'path');
        flow.classList.add('connector-flow');
        const padStart = document.createElementNS(svgNS, 'rect');
        padStart.classList.add('connector-pad');
        const padEnd = document.createElementNS(svgNS, 'rect');
        padEnd.classList.add('connector-pad');

        svg.appendChild(trace);
        svg.appendChild(padStart);
        svg.appendChild(padEnd);
        svg.appendChild(flow);

        return { trace, flow, padStart, padEnd, length: 0, anim: null };
    });

    function getLetterRect(index) {
        const range = document.createRange();
        range.setStart(textNode, index);
        range.setEnd(textNode, index + 1);
        return range.getClientRects()[0];
    }

    function setPad(rect, x, y) {
        rect.setAttribute('x', x - 2);
        rect.setAttribute('y', y - 2);
        rect.setAttribute('width', 4);
        rect.setAttribute('height', 4);
    }

    function update() {
        const containerRect = heroContent.getBoundingClientRect();
        svg.setAttribute('width', containerRect.width);
        svg.setAttribute('height', containerRect.height);
        svg.style.width = containerRect.width + 'px';
        svg.style.height = containerRect.height + 'px';

        for (let i = 0; i < 3; i++) {
            const titleRect = getLetterRect(i);
            const subRect = initials[i].getBoundingClientRect();
            if (!titleRect || !subRect) continue;

            const x1 = subRect.left + subRect.width / 2 - containerRect.left;
            const y1 = subRect.top - containerRect.top;
            const x2 = titleRect.left + titleRect.width / 2 - containerRect.left;
            const y2 = titleRect.bottom - containerRect.top;
            const midY = Math.max(y1 - BOTTOM_CLEARANCE - ROW_STAGGER[i], y2 + 12);

            const d = `M ${x1} ${y1} L ${x1} ${midY} L ${x2} ${midY} L ${x2} ${y2}`;
            const t = traces[i];
            t.trace.setAttribute('d', d);
            t.flow.setAttribute('d', d);
            setPad(t.padStart, x1, y1);
            setPad(t.padEnd, x2, y2);

            const length = t.flow.getTotalLength();
            const dash = Math.min(10, length * 0.2);
            const gap = Math.max(length - dash, 1);
            t.length = length;
            t.period = dash + gap;
            t.flow.style.strokeDasharray = `${dash} ${gap}`;
        }
    }

    const FLOW_SPEED = 110; // px per second, shared across all traces for a uniform pace

    function startFlow() {
        traces.forEach((t) => {
            if (t.anim) t.anim.cancel();
            const duration = Math.max(600, (t.period / FLOW_SPEED) * 1000);
            t.flow.style.strokeDashoffset = String(t.period);
            t.anim = t.flow.animate(
                [{ strokeDashoffset: t.period }, { strokeDashoffset: 0 }],
                { duration, iterations: Infinity, easing: 'linear' }
            );
        });
    }

    function stopFlow() {
        traces.forEach((t) => {
            if (t.anim) {
                t.anim.cancel();
                t.anim = null;
            }
        });
    }

    update();
    window.addEventListener('resize', update);
    if (document.fonts && document.fonts.ready) {
        document.fonts.ready.then(update);
    }

    subtitleFrame.addEventListener('mouseenter', () => {
        update();
        svg.classList.add('active');
        startFlow();
    });
    subtitleFrame.addEventListener('mouseleave', () => {
        svg.classList.remove('active');
        stopFlow();
    });
});
