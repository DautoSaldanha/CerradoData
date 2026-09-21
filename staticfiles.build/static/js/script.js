/* ==========================================================
   CERRADO DATA
   SCRIPT.JS
========================================================== */


/* ==========================================================
   HEADER AO ROLAR
========================================================== */

const header = document.getElementById("header");

if (header) {

    const updateHeader = () => {

        header.classList.toggle(
            "scrolled",
            window.scrollY > 40
        );

    };

    window.addEventListener(
        "scroll",
        updateHeader,
        { passive: true }
    );

    updateHeader();

}


/* ==========================================================
   MENU MOBILE
========================================================== */

const menuButton =
    document.getElementById("menuButton");

const nav =
    document.getElementById("nav");


if (menuButton && nav) {

    menuButton.addEventListener(
        "click",
        () => {

            const isOpen =
                nav.classList.toggle("active");

            menuButton.setAttribute(
                "aria-expanded",
                String(isOpen)
            );

            menuButton.setAttribute(
                "aria-label",
                isOpen
                    ? "Fechar menu"
                    : "Abrir menu"
            );

        }
    );

}


/* ==========================================================
   FECHAR MENU AO CLICAR EM LINK
========================================================== */

const navLinks =
    document.querySelectorAll(".nav__link");


navLinks.forEach((link) => {

    link.addEventListener(
        "click",
        () => {

            if (nav) {

                nav.classList.remove(
                    "active"
                );

            }

            if (menuButton) {

                menuButton.setAttribute(
                    "aria-expanded",
                    "false"
                );

                menuButton.setAttribute(
                    "aria-label",
                    "Abrir menu"
                );

            }

        }
    );

});


/* ==========================================================
   LINK ATIVO
========================================================== */

const sections =
    document.querySelectorAll(
        "section[id]"
    );


const updateActiveLink = () => {

    let current = "";

    const scrollPosition =
        window.scrollY + 180;


    sections.forEach((section) => {

        const sectionTop =
            section.offsetTop;

        const sectionBottom =
            sectionTop +
            section.offsetHeight;


        if (
            scrollPosition >= sectionTop &&
            scrollPosition < sectionBottom
        ) {

            current =
                section.getAttribute("id");

        }

    });


    navLinks.forEach((link) => {

        link.classList.toggle(
            "active",
            link.getAttribute("href") ===
            `#${current}`
        );

    });

};


if (sections.length) {

    window.addEventListener(
        "scroll",
        updateActiveLink,
        { passive: true }
    );

    updateActiveLink();

}


/* ==========================================================
   MODAL — APRESENTAÇÃO DA CERRADO DATA
========================================================== */

const presentationButton =
    document.getElementById(
        "presentationButton"
    );


const presentationModal =
    document.getElementById(
        "presentationModal"
    );


const closePresentationModal =
    document.getElementById(
        "closePresentationModal"
    );


const presentationProjectsLink =
    document.getElementById(
        "presentationProjectsLink"
    );


/* ==========================================================
   ABRIR MODAL
========================================================== */

function openPresentationModal() {

    if (!presentationModal) {
        return;
    }


    presentationModal.classList.add(
        "active"
    );


    presentationModal.setAttribute(
        "aria-hidden",
        "false"
    );


    document.body.style.overflow =
        "hidden";


    if (closePresentationModal) {

        closePresentationModal.focus();

    }

}


/* ==========================================================
   FECHAR MODAL
========================================================== */

function closePresentation() {

    if (!presentationModal) {
        return;
    }


    presentationModal.classList.remove(
        "active"
    );


    presentationModal.setAttribute(
        "aria-hidden",
        "true"
    );


    document.body.style.overflow = "";

}


/* ==========================================================
   BOTÃO DE APRESENTAÇÃO
========================================================== */

if (presentationButton) {

    presentationButton.addEventListener(
        "click",
        openPresentationModal
    );

}


/* ==========================================================
   BOTÃO FECHAR
========================================================== */

if (closePresentationModal) {

    closePresentationModal.addEventListener(
        "click",
        closePresentation
    );

}


/* ==========================================================
   IR PARA PROJETOS
========================================================== */

if (presentationProjectsLink) {

    presentationProjectsLink.addEventListener(
        "click",
        closePresentation
    );

}


/* ==========================================================
   FECHAR CLICANDO FORA
========================================================== */

if (presentationModal) {

    presentationModal.addEventListener(
        "click",
        (event) => {

            if (
                event.target ===
                presentationModal
            ) {

                closePresentation();

            }

        }
    );

}


/* ==========================================================
   FECHAR COM ESC
========================================================== */

document.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Escape" &&
            presentationModal?.classList.contains(
                "active"
            )
        ) {

            closePresentation();

        }

    }
);


/* ==========================================================
   FORMULÁRIO
========================================================== */

const contactForm =
    document.getElementById(
        "contactForm"
    );


const formMessage =
    document.getElementById(
        "formMessage"
    );


if (contactForm) {

    contactForm.addEventListener(
        "submit",
        (event) => {

            event.preventDefault();


            const name =
                document
                    .getElementById("name")
                    ?.value
                    .trim();


            const email =
                document
                    .getElementById("email")
                    ?.value
                    .trim();


            const message =
                document
                    .getElementById("message")
                    ?.value
                    .trim();


            if (
                !name ||
                !email ||
                !message
            ) {

                if (formMessage) {

                    formMessage.textContent =
                        "Preencha todos os campos.";

                }

                return;

            }


            if (formMessage) {

                formMessage.textContent =
                    "Mensagem preenchida com sucesso! Em breve entraremos em contato.";

            }


            contactForm.reset();

        }
    );

}


/* ==========================================================
   ANIMAÇÃO DE ENTRADA
========================================================== */

const animatedElements =
    document.querySelectorAll(
        ".service-card, .project, .about__content, .data-card"
    );


if (
    "IntersectionObserver" in window &&
    animatedElements.length
) {

    const observer =
        new IntersectionObserver(
            (entries) => {

                entries.forEach((entry) => {

                    if (
                        entry.isIntersecting
                    ) {

                        entry.target.style.opacity =
                            "1";


                        entry.target.style.transform =
                            "translateY(0)";


                        observer.unobserve(
                            entry.target
                        );

                    }

                });

            },
            {
                threshold: 0.12,
            }
        );


    animatedElements.forEach(
        (element) => {

            element.style.opacity =
                "0";


            element.style.transform =
                "translateY(25px)";


            element.style.transition =
                "opacity 0.7s ease, transform 0.7s ease";


            observer.observe(element);

        }
    );

} else {

    animatedElements.forEach(
        (element) => {

            element.style.opacity =
                "1";


            element.style.transform =
                "translateY(0)";

        }
    );

}