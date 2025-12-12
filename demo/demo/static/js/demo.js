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
    const blocks = document.querySelectorAll('.grid-block, .video-block, .card-block, .block-image, .carousel-block, .accordion-block, .tabs-block, .gallery-block, .timeline-block, .testimonial-block');
    blocks.forEach(el => {
        el.classList.add('reveal-on-scroll');
        observer.observe(el);
    });

    // ===== ACCORDION FUNCTIONALITY =====
    const accordionHeaders = document.querySelectorAll('.accordion-header');
    accordionHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const accordionBlock = header.closest('.accordion-block');
            const allowMultiple = accordionBlock.dataset.allowMultiple === 'True';
            const content = header.nextElementSibling;
            const isExpanded = header.getAttribute('aria-expanded') === 'true';

            // Close other accordions if allowMultiple is false
            if (!allowMultiple) {
                accordionBlock.querySelectorAll('.accordion-header').forEach(otherHeader => {
                    if (otherHeader !== header) {
                        otherHeader.setAttribute('aria-expanded', 'false');
                        otherHeader.nextElementSibling.classList.remove('active');
                    }
                });
            }

            // Toggle current accordion
            header.setAttribute('aria-expanded', !isExpanded);
            content.classList.toggle('active');
        });
    });

    // ===== TABS FUNCTIONALITY =====
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabsBlock = button.closest('.tabs-block');
            const tabIndex = button.dataset.tabIndex;

            // Remove active class from all tabs and panels
            tabsBlock.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active');
                btn.setAttribute('aria-selected', 'false');
            });
            tabsBlock.querySelectorAll('.tab-panel').forEach(panel => {
                panel.classList.remove('active');
            });

            // Add active class to clicked tab and corresponding panel
            button.classList.add('active');
            button.setAttribute('aria-selected', 'true');
            const activePanel = tabsBlock.querySelector(`.tab-panel[data-tab-index="${tabIndex}"]`);
            if (activePanel) {
                activePanel.classList.add('active');
            }
        });
    });

    // ===== GALLERY LIGHTBOX FUNCTIONALITY =====
    const galleryLinks = document.querySelectorAll('.gallery-link');
    let currentImageIndex = 0;
    let galleryImages = [];

    galleryLinks.forEach((link, index) => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const galleryBlock = link.closest('.gallery-block');
            if (galleryBlock.dataset.lightbox === 'True') {
                galleryImages = Array.from(galleryBlock.querySelectorAll('.gallery-link'));
                currentImageIndex = index;
                openLightbox(link.href);
            }
        });
    });

    function openLightbox(imageSrc) {
        let modal = document.getElementById('lightbox-modal');
        if (!modal) {
            // Create modal if it doesn't exist
            modal = document.createElement('div');
            modal.id = 'lightbox-modal';
            modal.className = 'lightbox-modal';
            modal.innerHTML = `
                <button class="lightbox-close" aria-label="Close lightbox">&times;</button>
                <button class="lightbox-prev" aria-label="Previous image">
                    <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
                        <path d="M25 10L15 20L25 30" stroke="white" stroke-width="3" stroke-linecap="round"/>
                    </svg>
                </button>
                <button class="lightbox-next" aria-label="Next image">
                    <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
                        <path d="M15 10L25 20L15 30" stroke="white" stroke-width="3" stroke-linecap="round"/>
                    </svg>
                </button>
                <div class="lightbox-content">
                    <img src="" alt="" class="lightbox-image">
                </div>
            `;
            document.body.appendChild(modal);

            // Add event listeners
            modal.querySelector('.lightbox-close').addEventListener('click', closeLightbox);
            modal.querySelector('.lightbox-prev').addEventListener('click', showPrevImage);
            modal.querySelector('.lightbox-next').addEventListener('click', showNextImage);
            modal.addEventListener('click', (e) => {
                if (e.target === modal) closeLightbox();
            });
        }

        const img = modal.querySelector('.lightbox-image');
        img.src = imageSrc;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
        const modal = document.getElementById('lightbox-modal');
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    function showPrevImage() {
        currentImageIndex = (currentImageIndex - 1 + galleryImages.length) % galleryImages.length;
        const img = document.querySelector('.lightbox-image');
        img.src = galleryImages[currentImageIndex].href;
    }

    function showNextImage() {
        currentImageIndex = (currentImageIndex + 1) % galleryImages.length;
        const img = document.querySelector('.lightbox-image');
        img.src = galleryImages[currentImageIndex].href;
    }

    // Keyboard navigation for lightbox
    document.addEventListener('keydown', (e) => {
        const modal = document.getElementById('lightbox-modal');
        if (modal && modal.classList.contains('active')) {
            if (e.key === 'Escape') closeLightbox();
            if (e.key === 'ArrowLeft') showPrevImage();
            if (e.key === 'ArrowRight') showNextImage();
        }
    });

    // ===== PARALLAX EFFECT =====
    const parallaxContainers = document.querySelectorAll('.parallax-container');
    if (parallaxContainers.length > 0) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            parallaxContainers.forEach(container => {
                const layers = container.querySelectorAll('.parallax-layer');
                layers.forEach((layer, index) => {
                    const speed = (index + 1) * 0.1;
                    const yPos = -(scrolled * speed);
                    layer.style.transform = `translateY(${yPos}px)`;
                });
            });
        });
    }

    // ===== SMOOTH PAGE TRANSITIONS =====
    const mainContent = document.querySelector('.site-main');
    if (mainContent) {
        mainContent.classList.add('page-transition');
    }

    // ===== STAGGERED GRID ANIMATIONS =====
    const gridItems = document.querySelectorAll('.grid-item, .gallery-item, .testimonial-item, .timeline-event');
    gridItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;
        item.classList.add('reveal-on-scroll');
        observer.observe(item);
    });

    // ===== ENHANCED CAROUSEL AUTO-PLAY =====
    const carousels = document.querySelectorAll('.carousel-block');
    carousels.forEach(carousel => {
        const slides = carousel.querySelectorAll('.carousel-slide');
        if (slides.length > 1) {
            let currentSlide = 0;
            const autoPlayInterval = 5000; // 5 seconds

            function showSlide(index) {
                slides.forEach((slide, i) => {
                    slide.style.display = i === index ? 'block' : 'none';
                });
            }

            function nextSlide() {
                currentSlide = (currentSlide + 1) % slides.length;
                showSlide(currentSlide);
            }

            // Initialize
            showSlide(0);

            // Auto-play
            setInterval(nextSlide, autoPlayInterval);

            // Add navigation buttons if they exist
            const prevBtn = carousel.querySelector('.carousel-prev');
            const nextBtn = carousel.querySelector('.carousel-next');

            if (prevBtn) {
                prevBtn.addEventListener('click', () => {
                    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
                    showSlide(currentSlide);
                });
            }

            if (nextBtn) {
                nextBtn.addEventListener('click', () => {
                    nextSlide();
                });
            }
        }
    });

    console.log('Navigation enhancements loaded successfully!');
});

