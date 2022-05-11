let stems = document.getElementsByClassName("myAudio");
let playButton = document.getElementById("play-button");
let sliders = document.getElementsByClassName("slider");

playButton.addEventListener("click", () => {
    // Working on a better way to do this. Not a fan of hardcoding numbers in
    if (stems[0].paused)
    {
        for (let i = 0; i < stems.length; i++)
            stems[i].play();
        playButton.innerHTML = "Pause";
    }
    else
    {
        for (let i = 0; i < stems.length; i++)
            stems[i].pause();
        playButton.innerHTML = "Play";
    }
});

// Adjusts volume based on slider range value
for (let i = 0; i < sliders.length; i++){
    sliders[i].oninput = () => stems[i].volume = sliders[i].value / 10;
}

