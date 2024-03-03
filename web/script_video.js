import {KEY_FILENAME} from './consts.js'


// ============ APP STATE
let app_state = {
    task_in_progress: false,
}

let getHistoryjkaFilename = () => localStorage.getItem(KEY_FILENAME)

let updateTaskInProgressStatus = (in_progress) => {
    app_state.task_in_progress = in_progress
    document.getElementById("render_button").disabled = in_progress
}


// ============ SCHEDULE VIDEO BUILD
let renderVideo = () => {
    if (app_state.task_in_progress) {
        return false
    }
    let historyjka_filename = getHistoryjkaFilename()
    let video_params = {
        video_name: document.getElementById("params_name").value,
        is_vertical: document.getElementById("params_is_vertical").checked
    }

    eel.render_video(historyjka_filename, video_params)(function (response) {
        if (response.success) {
            updateTaskInProgressStatus(true)
        } else {
            updateLogWindow([response.msg])
        }
    })
}
document.getElementById("render_button").onclick = renderVideo


// ============ UPDATE DATA
window.addEventListener("load", (event) => {
    let filename = getHistoryjkaFilename()
    let historyjka_name = filename.replace('.json', "")
    document.getElementById("navbar_name").innerText = historyjka_name
    document.getElementById("params_name").value = historyjka_name
    checkTaskStatus()
})

// Fetch logs
let updateLogWindow = (logs) => {
    if (logs.length === 0) return
    let log_window = document.getElementById("video_log")
    log_window.innerHTML = logs.map(log => `<div>${log}</div>`).join('')
}

let fetchAndUpdateTaskLog = () => {
    if (!app_state.task_in_progress) return

    eel.get_video_task_logs(
        getHistoryjkaFilename()
    )(updateLogWindow)
}

setInterval(function () {
    if (!app_state.task_in_progress) return

    fetchAndUpdateTaskLog()
}, 500);

// Check if task finished
let checkTaskStatus = () => {
    eel.get_video_task_liveness(
        getHistoryjkaFilename()
    )((is_alive) => {
        fetchAndUpdateTaskLog()
        updateTaskInProgressStatus(is_alive)
    })
}

setInterval(function () {
    if (!app_state.task_in_progress) return
    checkTaskStatus()

}, 600);


// ============ NAVBAR CONTROLS
let redirectToStoryList = () => {
    window.location = 'index.html'
}
document.getElementById("navbar_back").onclick = redirectToStoryList