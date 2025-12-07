function updateStylesInefficiently() {
    const element = document.getElementById("my-box");

    for(let i=0; i < 100; i++) {
        const currentWidth = element.offsetWidth;

        element.style.width = (currentWidth + 1) + 'px';
    }
}

updateStylesInefficiently();

function updateStylesEfficiently() {
    const element = document.getElementById("my-box");
    let currentWidth = element.offsetWidth;

    for(let i=0; i < 100; i++) {
        currentWidth += 1;
    }

    element.style.width = currentWidth + "px";
}

updateStylesEfficiently();