document.addEventListener("DOMContentLoaded", function () {

    const themeButton = document.getElementById("themeButton");

    // Load saved dark mode
    const darkMode = localStorage.getItem("careerportal-dark-mode");

    if (darkMode === "enabled") {
        document.body.classList.add("dark-mode");

        if (themeButton) {
            themeButton.textContent = "☀️";
        }
    } else {
        if (themeButton) {
            themeButton.textContent = "🌙";
        }
    }

    // Theme button
    if (themeButton) {

        themeButton.addEventListener("click", function () {

            document.body.classList.toggle("dark-mode");

            if (document.body.classList.contains("dark-mode")) {

                localStorage.setItem(
                    "careerportal-dark-mode",
                    "enabled"
                );

                themeButton.textContent = "☀️";

            } else {

                localStorage.setItem(
                    "careerportal-dark-mode",
                    "disabled"
                );

                themeButton.textContent = "🌙";
            }

        });

    }

});