async function loadMods() {
    const mods = await window.pywebview.api.get_mods()

    const enabled = mods[0]
    const disabled = mods[1]

    const enabledDiv = document.getElementById("enabled")
    const disabledDiv = document.getElementById("disabled")

    enabledDiv.innerHTML = ""
    disabledDiv.innerHTML = ""

    for (const mod of enabled) {
        const button = document.createElement("button")
        button.innerText = mod

        button.onclick = async function () {
            await window.pywebview.api.disable_mod(mod)
            loadMods()
        }

        enabledDiv.appendChild(button)
    }

    for (const mod of disabled) {
        const button = document.createElement("button")
        button.innerText = mod

        button.onclick = async function () {
            await window.pywebview.api.enable_mod(mod)
            loadMods()
        }

        disabledDiv.appendChild(button)
    }
}

async function launchGame() {
    await window.pywebview.api.launch_game()
}

async function updateLaunchButton() {
    const running = await window.pywebview.api.is_game_running()
    const button = document.getElementById("launch-button")

    if (running) {
        button.innerText = "Restart Game to Reload Mods"
    } else {
        button.innerText = "Launch Game"
    }
}

window.addEventListener("pywebviewready", function () {
    loadMods()
    updateLaunchButton()

    setInterval(updateLaunchButton, 1000)
})