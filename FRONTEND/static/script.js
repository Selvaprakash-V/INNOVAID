document.addEventListener("DOMContentLoaded", () => {
    // Smooth scrolling for navigation links
    document.querySelectorAll('.nav-links a').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: "smooth"
                });
            }
        });
    });

    // Form Validation
    const form = document.querySelector('.contact-form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const message = document.getElementById('message').value.trim();
        const checkbox = document.querySelector('.contact-form input[type="checkbox"]');

        if (name === "" || email === "" || message === "") {
            alert("Please fill in all fields.");
            return;
        }

        if (!checkbox.checked) {
            alert("You must accept the terms to continue.");
            return;
        }

        alert("Form submitted successfully!");
        form.reset();
    });

    // Animation on scroll
    const elements = document.querySelectorAll('.solution-card');
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.transform = "scale(1.05)";
                entry.target.style.transition = "0.3s";
            } else {
                entry.target.style.transform = "scale(1)";
            }
        });
    }, { threshold: 0.5 });

    elements.forEach(el => observer.observe(el));
});
