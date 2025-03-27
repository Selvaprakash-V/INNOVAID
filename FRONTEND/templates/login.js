// Page Load Animation
document.addEventListener("DOMContentLoaded", function () {
    anime({
        targets: ".card",
        translateY: [ -50, 0 ],
        opacity: [0, 1],
        duration: 1000,
        easing: "easeOutExpo"
    });
});

// Handle Form Submission
document.getElementById("loginForm").addEventListener("submit", function (event) {
    event.preventDefault();
    alert("Login Successful!");
});
