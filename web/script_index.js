import {KEY_FILENAME} from './consts.js'


window.addEventListener("load", (event) => {
    eel.get_saved_stories()(loadStoriesToUi)
    console.log("Loaded stories list");
});

let loadStoriesToUi = (stories_filenames) => {
    let scenario_list_elem = document.getElementById("stories_list")
    stories_filenames.forEach(filename => {
        let single_scenario_elem = document.createElement('li')
        single_scenario_elem.onclick = () => redirectToStoryEditor(filename)
        single_scenario_elem.innerText = filename.replace('.json', '')

        scenario_list_elem.appendChild(single_scenario_elem)
    })
}

let redirectToStoryEditor = (story_filename) => {
    localStorage.setItem(KEY_FILENAME, story_filename)
    window.location = 'editor.html'
}