const appState = {}
const content = document.getElementById('content')
const nav = document.getElementById('jokes-nav')

const updateNav = () => {
    const backToJokes = document.createElement('li')
    const a = document.createElement('a')
    a.id = 'back-to-jokes'
    a.textContent = 'Powrut do dowcipuw'
    a.classList.add('special_link')
    a.addEventListener('click', handleBack)
    backToJokes.appendChild(a)
    nav.querySelector('ul').appendChild(backToJokes)
}

const handleBack = () => {
    clearAllIntervals()
    removeElementById('back-to-jokes')
    displayJokesData()
}

const clearAllIntervals = () => {
    Object.keys(appState).forEach(jokeId => {
        clearInterval(appState[jokeId].intervalId)
    })
}

const clearContent = (n = 0) => {
    while (content.lastChild) {
        if (content.children.length === n) {
            break
        }
        content.removeChild(content.lastChild);
    }
}

const displayJokesData = () => {
    clearContent()
    eel.get_jokes_data()((jokes) => {
        const table = document.createElement('table');

        const thead = document.createElement('thead');
        const headerRow = thead.insertRow();
        ['jokeId', 'Tytuł', 'videoId'].forEach(key => {
            const th = document.createElement('th');
            th.textContent = key;
            headerRow.appendChild(th);
        })
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        Object.keys(jokes).forEach(jokeId => {
            const row = tbody.insertRow()
            row.id = jokeId

            const idCell = row.insertCell()
            idCell.textContent = jokeId

            const titleCell = row.insertCell()
            titleCell.textContent = jokes[jokeId].title

            const videoIdCell = row.insertCell()
            videoIdCell.textContent = jokes[jokeId].videoId

            row.addEventListener('click', handleJokeClick)
        })
        table.appendChild(tbody)
        content.appendChild(table)

        const button = document.createElement('button')
        button.textContent = 'Dodaj nowy dowcip'
        button.classList.add('special_button')
        button.addEventListener('click', addJoke)
        content.appendChild(button)
    })
}

const refreshJoke = (jokeId) => {
    const button = document.createElement('button')
    button.id = jokeId
    button.addEventListener('click', handleJokeClick)
    button.click()
}

const handleJokeClick = async (event) => {
    updateNav()
    clearContent()
    const jokeId = event.currentTarget.id
    eel.get_joke_detail(jokeId)(data => {
        if (!data) {
            const p = document.createElement('p')
            p.textContent = `Dowcip "${jokeId}" nie istnieje.`
        } else {
            console.log(data)
            const deleteButton = document.createElement('button')
            deleteButton.textContent = 'Usuń dowcip'
            deleteButton.classList.add('special_button')
            deleteButton.addEventListener('click', () => {
                deleteJoke(jokeId)
            })
            content.appendChild(deleteButton)

            const title = document.createElement('p')
            title.textContent = `Tytuł: ${data.title}`

            const rawText = document.createElement('div')
            rawText.innerText = `Niesparsowany:\n${data.raw}`

            const parsedText = document.createElement('div')
            parsedText.innerText = `Sparsowany:\n${data.parsed}`

            content.appendChild(title)
            content.appendChild(rawText)
            content.appendChild(document.createElement('br'))
            content.appendChild(parsedText)

            const isUploaded = data.videoId ? true : false
            if (!data.isVideoRendered) {
                eel.get_video_task_liveness(jokeId)(isAlive => {
                    if (isAlive) {
                        startTaskInterval(jokeId)
                    } else {
                        addRenderButton(jokeId)
                    }
                })
            } else {
                addRenderedVideo(jokeId, isUploaded)
                if (!isUploaded) {
                    addUploadForm(jokeId, true)
                } else {
                    addYoutubeData(data.videoId, data.youtube)
                }
            }
        }
    })
}

const addWindowLog = () => {
    const logWindow = document.createElement('div')
    logWindow.id = 'log-window'
    logWindow.classList.add('window-log-jokes')
    content.appendChild(logWindow)
}

const addRenderButton = (jokeId) => {
    if (!document.getElementById('render-button')) {
        const renderButton = document.createElement('button')
        renderButton.id = 'render-button'
        renderButton.classList.add('special_button')
        renderButton.textContent = 'Renderuj dowcip'
        renderButton.addEventListener('click', () => {
            renderJoke(jokeId)
        })
        content.appendChild(renderButton)
    }
}

const addUploadForm = (jokeId) => {
    let currentStatus = 'public'
    const statusCheck = document.getElementById('status-select')
    if (statusCheck) {
        currentStatus = statusCheck.value
    }

    removeElementById('upload-form')

    const form = document.createElement('form')
    form.id = 'upload-form'
    form.classList.add('flex-col')

    const statusSelect = document.createElement('select')
    statusSelect.id = 'status-select'
    const statuses = ['public', 'private']
    statuses.forEach(status => {
        const option = document.createElement('option')
        option.value = status
        option.textContent = status
        if (currentStatus === status) {
            option.selected = true
        }
        statusSelect.appendChild(option)
    })

    statusSelect.classList.add('special_input')
    statusSelect.addEventListener('change', () => {
        addUploadForm(jokeId)
    })

    form.appendChild(statusSelect)

    const publishTime = document.createElement('input')
    publishTime.id = 'publish-time'
    publishTime.type = 'datetime-local'
    publishTime.classList.add('special_input')
    const currentDate = new Date().toISOString().slice(0, 16)
    publishTime.min = currentDate
    if (currentStatus === 'private') {
        form.appendChild(publishTime)
    }

    const uploadButton = document.createElement('button')
    uploadButton.textContent = 'Uploaduj dowcip'
    uploadButton.type = 'submit'
    uploadButton.classList.add('special_button')
    form.appendChild(uploadButton)

    form.addEventListener('submit', (event) => {
        event.preventDefault()
        const publishTimeISO = publishTime.value ? new Date(publishTime.value).toISOString() : null
        console.log(jokeId, statusSelect.value, publishTimeISO)
        uploadJoke(jokeId, statusSelect.value, publishTimeISO)
    })

    content.append(form)
}

const addRenderedVideo = (jokeId, isUploaded) => {
    eel.get_video_base64(jokeId)(base64video => {
        const videoContainer = document.createElement('div')
        videoContainer.id = 'video-container'

        const video = document.createElement('video')
        video.width = 640
        video.height = 480
        video.controls = true
        video.src = base64video
        videoContainer.appendChild(video)

        if (!isUploaded) {
            const deleteVideoButton = document.createElement('button')
            deleteVideoButton.textContent = 'Usuń wideo'
            deleteVideoButton.classList.add('special_button')
            deleteVideoButton.addEventListener('click', () => {
                deleteVideo(jokeId)
            })
            videoContainer.appendChild(deleteVideoButton)
        }

        const uploadForm = document.getElementById('upload-form')
        if (uploadForm) {
            content.insertBefore(videoContainer, uploadForm)
        } else {
            content.appendChild(videoContainer)
        }
    })
}

const addYoutubeData = (videoId, youtubeData) => {
    const youtubeContainer = document.createElement('div')
    if (youtubeData.status === 'public') {
        const frame = document.createElement('iframe')
        frame.src = `https://www.youtube.com/embed/${videoId}`
        frame.width = 640
        frame.height = 480
        frame.allowfullscreen = true
        frame.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        youtubeContainer.appendChild(frame)
    } else if (youtubeData.publishedAt) {
        const dateObj = new Date(youtubeData.publishedAt);

        const day = String(dateObj.getUTCDate()).padStart(2, '0');
        const month = String(dateObj.getUTCMonth() + 1).padStart(2, '0');
        const year = dateObj.getUTCFullYear();

        const hours = String(dateObj.getUTCHours()).padStart(2, '0');
        const minutes = String(dateObj.getUTCMinutes()).padStart(2, '0');

        const p = document.createElement('p')
        p.textContent = `Data premiery filmu: ${day}-${month}-${year} ${hours}:${minutes}`
        youtubeContainer.appendChild(p)
    } else {
        const p = document.createElement('p')
        p.textContent = `Wideo jest prywatne.`
        youtubeContainer.appendChild(p)
    }
    content.appendChild(youtubeContainer)
}

const removeElementById = (elementId) => {
    const element = document.getElementById(elementId)
    if (element) {
        element.remove()
    }
}

const renderJoke = (jokeId) => {
    document.getElementById('render-button').disabled = true
    eel.render_joke_video(jokeId)((response) => {
        if (response.success) {
            removeElementById('render-button')
            startTaskInterval(jokeId)
        } else {
            window.alert(response.msg)
        }
    })
}

const startTaskInterval = (jokeId) => {
    const intervalId = setInterval(() => {
        checkTaskStatus(jokeId)
    }, 1000)
    appState[jokeId] = { intervalId }
}

const checkTaskStatus = (jokeId) => {
    eel.get_video_task_liveness(jokeId)(isAlive => {
        if (isAlive) {
            fetchAndUpdateTaskLog(jokeId)
        } else {
            clearAllIntervals()
            removeElementById('log-window')
            addRenderedVideo(jokeId)
            addUploadForm(jokeId)
        }
    })
}

let fetchAndUpdateTaskLog = (jokeId) => {
    let logWindow = document.getElementById('log-window')
    if (!logWindow) {
        addWindowLog()
        logWindow = document.getElementById('log-window')
    }
    eel.get_video_task_logs(jokeId)(logs => {
        logWindow.innerHTML = null
        logs.forEach(log => {
            const p = document.createElement('p')
            p.textContent = log
            logWindow.appendChild(p)
        })
    })
}

const uploadJoke = (jokeId, status, publishTime) => {
    eel.upload_joke(jokeId, status, publishTime)((videoId, videoData) => {
        console.log('upload done', videoId, videoData)
        removeElementById('upload-form')
        addYoutubeData(videoId, videoData)
    })
}

const addJoke = () => {
    clearContent()
    eel.get_jokes_categories()(categories => {

        const label = document.createElement('label')
        label.textContent = 'Kategoria dowcipu:'

        const categorySelect = document.createElement('select')
        categorySelect.classList.add('special_input')
        categorySelect.id = 'category-select'

        categories.forEach((category) => {
            const option = document.createElement('option')
            option.text = category
            option.value = category
            categorySelect.appendChild(option)
        })

        categorySelect.selectedIndex = -1

        content.appendChild(label)
        content.appendChild(categorySelect)
        categorySelect.addEventListener('change', addJokeSelect)
    })
}

const addJokeSelect = (event) => {
    clearContent(2)
    const jokeCategory = event.target.value
    eel.get_available_jokes_for_category(jokeCategory)((jokes) => {
        const label = document.createElement('label')
        label.textContent = 'Dowcip:'

        const jokeSelect = document.createElement('select')
        jokeSelect.classList.add('special_input')
        jokeSelect.id = 'joke-select'

        jokes.forEach((joke) => {
            const option = document.createElement('option')
            option.text = joke
            option.value = joke
            jokeSelect.appendChild(option)
        })

        jokeSelect.selectedIndex = -1

        content.appendChild(label)
        content.appendChild(jokeSelect)
        jokeSelect.addEventListener('change', getJokeRaw)
    })
}

const getJokeRaw = (event) => {
    clearContent(4)
    const category = document.getElementById('category-select').value
    const filename = event.target.value
    eel.get_joke_raw(category, filename)((jokeText) => {
        const paragraph = document.createElement('p')
        paragraph.innerText = jokeText
        content.appendChild(paragraph)

        const nextButton = document.createElement('button')
        nextButton.classList.add('special_button')
        nextButton.innerText = 'parsuj to'
        nextButton.addEventListener('click', parseRawJoke)
        content.appendChild(nextButton)
    })
}

const parseRawJoke = () => {
    const category = document.getElementById('category-select').value
    const joke = document.getElementById('joke-select').value
    eel.parse_joke(category, joke)((jokeParsed) => {
        const textArea = document.createElement('textarea')
        textArea.id = 'parsed-joke-input'
        textArea.style = 'height: 300px'
        textArea.classList.add('special_input')
        textArea.value = jokeParsed
        content.appendChild(textArea)

        const label = document.createElement('label')
        label.innerText = 'Tytuł:'
        const titleInput = document.createElement('input')
        titleInput.style = 'width: 100%'
        titleInput.classList.add('special_input')
        titleInput.id = 'title-input'
        label.appendChild(titleInput)
        content.appendChild(label)

        const button = document.createElement('button')
        button.innerText = 'Dodaj dowcip'
        button.classList.add('special_button')
        button.addEventListener('click', saveJokeData)
        content.appendChild(button)
    })
}

const saveJokeData = () => {
    const category = document.getElementById('category-select').value
    const joke = document.getElementById('joke-select').value
    const title = document.getElementById('title-input').value
    const parsedJoke = document.getElementById('parsed-joke-input').value
    eel.add_new_joke(category, joke, title, parsedJoke)(() => {
        displayJokesData()
    })
}

const deleteJoke = (jokeId) => {
    eel.delete_joke(jokeId)(() => {
        displayJokesData()
    })
}

const deleteVideo = (jokeId) => {
    eel.delete_joke_video(jokeId)(() => {
        document.getElementById('video-container').remove()
        addRenderButton(jokeId)
    })
}

window.onload = () => {
    displayJokesData()
}