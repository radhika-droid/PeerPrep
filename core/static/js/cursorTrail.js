document.addEventListener("DOMContentLoaded", () => {
    const trailLength = 10; // number of dots in snake
    const dots = [];

    for (let i = 0; i < trailLength; i++) {
        const dot = document.createElement("div");
        dot.className = "cursor-dot";
        document.body.appendChild(dot);
        dots.push(dot);
    }

    let mouseX = 0, mouseY = 0;

    document.addEventListener("mousemove", (e) => {
        mouseX = e.pageX;
        mouseY = e.pageY;
    });

    function animateTrail() {
        let x = mouseX, y = mouseY;

        dots.forEach((dot, index) => {
            setTimeout(() => {
                dot.style.left = `${x}px`;
                dot.style.top = `${y}px`;
            }, index * 30); // delay for snake effect
        });

        requestAnimationFrame(animateTrail);
    }

    animateTrail();
});
