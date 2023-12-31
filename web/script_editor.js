import {KEY_FILENAME} from './consts.js'

const CHARACTER_DETAILS_ID_PREFIX = "character_details_"
const CHARACTER_FACE_SELECT_ID_PREFIX = "character_select_photo_"
const CHARACTER_GENDER_SELECT_ID_PREFIX = "character_select_gender_"
const CHARACTER_SKIN_SELECT_ID_PREFIX = "character_select_skin_"
const SCENARIO_RAW_ID = "scenario_raw"


// ============ APP STATE
let app_state = {
    scenario: [],
    actors: [], // actors in scenario
    characters: {}, // all characters
    available_characters_photos: [],
    available_characters_skins: [],
}

let updateAppStateWithParsedScenario = (parsed_data) => {
    app_state.scenario = parsed_data.parsed_story.scenario
    app_state.actors = parsed_data.parsed_story.actors
    app_state.characters = parsed_data.characters
}

// ============ PARSED ELEMENTS
let updateCharacters = () => {
    // Add or update character details
    // TODO: this is disgusting :0
    let characters_list_elem = document.getElementById("character_details_list")
    app_state.actors.forEach(name => {
        let character_data = app_state.characters[name]
        let character_element = document.getElementById(`${CHARACTER_DETAILS_ID_PREFIX}${name}`)

        if (character_element !== null) {
            // Update existing characters details
        } else {
            // Add a new character
            let new_character_element_raw = `
              <div class="character_details" id="${CHARACTER_DETAILS_ID_PREFIX}${name}">
                <span class="character_name">${name}</span>
                <div class="character_details_edit">
                    gender:
                    <select class="character_img_select" id="${CHARACTER_GENDER_SELECT_ID_PREFIX}${name}">
                      <option value="MALE" ${character_data.gender === "MALE" ? 'selected="selected"' : ""}>M</option>
                      <option value="FEMALE" ${character_data.gender === "FEMALE" ? 'selected="selected"' : ""}>F</option>
                    </select>
                    photo:
                    <select class="character_img_select" id="${CHARACTER_FACE_SELECT_ID_PREFIX}${name}">
                      <option value="${character_data.face_image}">${character_data.face_image}</option>
                      ${app_state.available_characters_photos.map(image_name => `
                                  <option value="${image_name}">
                                    ${image_name}
                                  </option>
                                `)}
                    </select>
                    skin:
                    <select class="character_img_select" id="${CHARACTER_SKIN_SELECT_ID_PREFIX}${name}">
                      <option value="${character_data.skin_image}">${character_data.skin_image}</option>
                      ${app_state.available_characters_skins.map(image_name => `
                                  <option value="${image_name}">
                                    ${image_name}
                                  </option>
                                `)}
                    </select>
                </div>
              </div>
            `
            characters_list_elem.innerHTML += new_character_element_raw
        }
    })

    // Remove characters if they no longer exist in the story
    let existing_characters_names = getCharactersNamesInCharactersDetailsList()
    existing_characters_names.forEach(existing_name => {
        if (!app_state.actors.includes(existing_name)) {
            document.getElementById(`${CHARACTER_DETAILS_ID_PREFIX}${existing_name}`).remove()

        }
    })
}

let updateParsedStory = () => {
    document.querySelector("#parsed_story").innerHTML = app_state.scenario.map(scenario_elem => {
        if (scenario_elem.actor && scenario_elem.content) {
            return `<div><span style=${characterNameToStyle(scenario_elem.actor)}>${scenario_elem.actor}:</span> ${scenario_elem.content}</div>`;
        } else if (scenario_elem.actor && scenario_elem.action) {
            return `<div>[<span style=${characterNameToStyle(scenario_elem.actor)}>${scenario_elem.actor}</span> action: ${scenario_elem.action}]</div>`;
        } else {
            return `<div>${scenario_elem.content}</div>`;
        }
    }).join('');
}

let characterNameToStyle = (actor_name) => {
    let actor_factor = app_state.actors.indexOf(actor_name) / app_state.actors.length
    let H = Math.floor(actor_factor * 300)
    return `"color: hsl(${H}, 60%, 40%); font-weight: bold"`
}

let overrideRawText = (raw_story) => {
    let raw_story_element = document.getElementById(SCENARIO_RAW_ID)
    raw_story_element.value = raw_story
}

let updateEditorWithParsedData = (parsed_data, reload_raw_story = false) => {
    if (reload_raw_story) {
        overrideRawText(parsed_data.raw_story)
    }
    updateAppStateWithParsedScenario(parsed_data)
    updateParsedStory()
    updateCharacters()
}

// ============ UPDATE DATA
// init state on load; check the available photos
window.addEventListener("load", (event) => {
    let filename = localStorage.getItem(KEY_FILENAME)
    document.getElementById("navbar_name").innerText = filename.replace('.json', "")

    eel.get_characters_faces()(function (photos) {
        app_state.available_characters_photos = photos
    })
    eel.get_characters_skins()(function (photos) {
        app_state.available_characters_skins = photos
    })

    eel.load_historyjka_editor(filename)(
        ((parsed_data) => {
            updateEditorWithParsedData(parsed_data, true)
        })
    )
})


// periodically checks the raw scenario textedit and updates parsed story and editable elements
setInterval(function () {
    let scenario_raw = document.getElementById(SCENARIO_RAW_ID).value
    let characters_overrides = getCharactersEditToCharactersOverridePayload()

    eel.parse_scenario(
        scenario_raw,
        characters_overrides
    )(updateEditorWithParsedData)
}, 1000);


let getCharactersEditToCharactersOverridePayload = () => {
    let characters_override_payload = []

    getCharactersNamesInCharactersDetailsList().forEach(character_name => {
        let character_face_image = document.getElementById(CHARACTER_FACE_SELECT_ID_PREFIX + character_name).value
        let character_skin_image = document.getElementById(CHARACTER_SKIN_SELECT_ID_PREFIX + character_name).value
        let character_gender = document.getElementById(CHARACTER_GENDER_SELECT_ID_PREFIX + character_name).value

        characters_override_payload.push({
            name: character_name,
            face_image: character_face_image,
            skin_image: character_skin_image,
            gender: character_gender
        })
    })

    return characters_override_payload
}

let getCharactersNamesInCharactersDetailsList = () => {
    let characters_names = []
    let characters_details_elements = document.getElementById("character_details_list").children

    for (let i = 0; i < characters_details_elements.length; i++) {
        let character_details_elem = characters_details_elements[i]
        let character_name = character_details_elem.id.replace(CHARACTER_DETAILS_ID_PREFIX, '')
        characters_names.push(character_name)
    }

    return characters_names
}

// ============ NAVBAR CONTROLS
let redirectToStoryList = () => {
    window.location = 'index.html'
}
document.getElementById("navbar_back").onclick = redirectToStoryList