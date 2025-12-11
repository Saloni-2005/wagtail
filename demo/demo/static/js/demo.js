document.addEventListener('DOMContentLoaded', () => {
    // Scroll Reveal Animation
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, observerOptions);

    const elements = document.querySelectorAll('.reveal-on-scroll');
    elements.forEach(el => observer.observe(el));

    // Optional: Add reveal class to blocks automatically if they don't have it
    // This assumes specific block classes exist in your templates
    const blocks = document.querySelectorAll('.grid-block, .video-block, .card-block, .block-image');
    blocks.forEach(el => {
        el.classList.add('reveal-on-scroll');
        observer.observe(el);
    });
});
