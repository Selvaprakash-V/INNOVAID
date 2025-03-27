document.addEventListener("DOMContentLoaded", function () {
    let selectedRole = ""; // Store selected role

    // Get role buttons
    const roleButtons = document.querySelectorAll(".role-btn");

    // Add event listener to each button
    roleButtons.forEach(button => {
        button.addEventListener("click", function () {
            // Remove 'selected' class from all buttons
            roleButtons.forEach(btn => btn.classList.remove("selected"));

            // Add 'selected' class to clicked button
            this.classList.add("selected");

            // Store selected role in hidden input
            selectedRole = this.getAttribute("data-role");
            document.getElementById("role").value = selectedRole;
        });
    });

    // Form Submission
    document.getElementById("signupForm").addEventListener("submit", function (event) {
        event.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const role = document.getElementById("role").value;

        if (!role) {
            alert("Please select either Administrator or Customer!");
            return;
        }

        console.log(`Role: ${role}, Username: ${username}, Password: ${password}`);
        alert(`Signup successful as ${role}!`);
    });
});
