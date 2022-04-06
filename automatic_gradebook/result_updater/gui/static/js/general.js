
function closeOverlay() {
    let overlays = document.getElementsByClassName("overlay");
    if (overlays.length > 0)
        overlays[0].parentNode.removeChild(overlays[0]);
}