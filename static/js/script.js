const dynamicImage = document.getElementById("user-pic");

            window.addEventListener("scroll", () => {
            const scrollY = window.scrollY;

            // Si el usuario ha bajado más de 200px
            if (scrollY > 200) {
                dynamicImage.classList.add("fixed");
                dynamicImage.classList.remove("default");
            } else {
                dynamicImage.classList.add("default");
                dynamicImage.classList.remove("fixed");
            }
            });