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
        button.className = "mod-button"

        button.onclick = async function () {
            await window.pywebview.api.disable_mod(mod)
            loadMods()
        }

        enabledDiv.appendChild(button)
    }

    for (const mod of disabled) {
        const button = document.createElement("button")
        button.innerText = mod
        button.className = "mod-button"

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

async function loadSplitCategories() {
    const categories = await window.pywebview.api.get_split_categories()
    const active = await window.pywebview.api.get_active_split_category()

    const container = document.getElementById("split-categories")
    container.innerHTML = ""

    for (const category of categories) {
        const row = document.createElement("div")
        row.className = "split-row"

        const categoryButton = document.createElement("button")
        categoryButton.className = "category-button"

        if (category === active) {
            categoryButton.innerText = category + " (Active)"
        } else {
            categoryButton.innerText = category
        }

        categoryButton.onclick = async function () {
            await window.pywebview.api.set_active_split_category(category)
            loadSplitCategories()
        }

        const removeButton = document.createElement("button")
        removeButton.innerText = "Remove"
        removeButton.className = "remove-button"

        removeButton.onclick = async function () {
            const confirmed = confirm("Delete " + category + "?")

            if (!confirmed) {
                return
            }

            await window.pywebview.api.remove_split_category(category)
            loadSplitCategories()
        }

        row.appendChild(categoryButton)
        row.appendChild(removeButton)

        container.appendChild(row)
    }
}

async function addSplitCategory() {
    const name = prompt("Category name:")

    if (!name) {
        return
    }

    await window.pywebview.api.add_split_category(name)
    loadSplitCategories()
}

window.addEventListener("pywebviewready", function () {
    loadMods()
    loadSplitCategories()
    updateLaunchButton()

    setInterval(updateLaunchButton, 1000)
})