import {KEY_FILENAME} from './consts.js'

const STORIES_LIST_ID = "stories_list"
const STORY_LIST_ELEM_ID_PREFIX = "story_element_"


window.addEventListener("load", (event) => {
    eel.get_saved_stories()(loadStoriesToUi)
    console.log("Loaded stories list");
});

let filenameToListElementId = (filename) => {
    return STORY_LIST_ELEM_ID_PREFIX + filename.replace('.', '_')
}

let loadStoriesToUi = (stories_filenames) => {
    let scenario_list_elem = document.getElementById(STORIES_LIST_ID)
    stories_filenames.forEach(filename => {
        let single_scenario_elem = document.createElement('li')
        single_scenario_elem.id = filenameToListElementId(filename)

        let text_span = document.createElement("span");
        text_span.className = "stories_list_name"
        text_span.textContent = filename.replace('.json', '');

        let buttons_div = document.createElement("div");
        buttons_div.className = "stories_list_buttons"
        let edit_button = document.createElement("button");
        edit_button.innerText = "Edit"
        edit_button.className = "stories_list_button"
        edit_button.onclick = () => redirectToStoryEditor(filename)
        let video_button = document.createElement("button");
        video_button.innerText = "Video"
        video_button.className = "stories_list_button"
        video_button.onclick = () => redirectToVideoEditor(filename)
        let copy_button = document.createElement("button");
        copy_button.innerText = "Branch out"
        copy_button.className = "stories_list_button"
        copy_button.onclick = () => createStoryCopy(filename)
        let delete_button = document.createElement("button");
        delete_button.innerText = "Delete"
        delete_button.className = "stories_list_button"
        delete_button.onclick = () => deleteStory(filename)

        buttons_div.appendChild(edit_button)
        buttons_div.appendChild(video_button)
        buttons_div.appendChild(copy_button)
        buttons_div.appendChild(delete_button)

        single_scenario_elem.appendChild(text_span)
        single_scenario_elem.appendChild(buttons_div)

        scenario_list_elem.appendChild(single_scenario_elem)
    })
}

let addNewStory = () => {
    let story_name = prompt("Story name: ", "")
    if (!story_name) return

    let story_filename = story_name + '.json'
    redirectToStoryEditor(story_filename)
}
document.getElementById("new_story_button").onclick = addNewStory


let createStoryCopy = (story_filename) => {
    let new_story_name = prompt("Story name: ", "")
    if (!new_story_name) return

    let new_story_filename = new_story_name + '.json'
    eel.create_story_copy(story_filename, new_story_filename)(() => {
        redirectToStoryEditor(new_story_filename)
    })
}

let redirectToStoryEditor = (story_filename) => {
    localStorage.setItem(KEY_FILENAME, story_filename)
    window.location = 'editor.html'
}

let redirectToVideoEditor = (story_filename) => {
    localStorage.setItem(KEY_FILENAME, story_filename)
    window.location = 'video.html'
}

let deleteStory = (filename) => {
    if (confirm("Are you sure you want to delete this historyjka?")) {
        eel.remove_story(filename)(() => {
            let story_elem = document.getElementById(filenameToListElementId(filename))
            story_elem.remove()
        })
    }
}