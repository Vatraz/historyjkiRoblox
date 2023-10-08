const CHARACTER_DETAILS_ID_PREFIX = "character_details_"
const CHARACTER_FACE_SELECT_ID_PREFIX = "character_select_photo_"
const CHARACTER_SKIN_SELECT_ID_PREFIX = "character_select_skin_"


// ============ APP STATE
let app_state = {
    scenario: [],
    actors: [], // actors in scenario
    characters: {}, // all characters
    available_characters_photos: [],
    available_characters_skins: [],
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
                <select class="character_img_select" id="${CHARACTER_FACE_SELECT_ID_PREFIX}${name}">
                  <option value="${character_data.face_image}">${character_data.face_image}</option>
                  ${app_state.available_characters_photos.map(
                image_name => `
                      <option value="${image_name}">
                        ${image_name}
                      </option>
                    `
            )}
                </select>
                <select class="character_img_select" id="${CHARACTER_SKIN_SELECT_ID_PREFIX}${name}">
                  <option value="${character_data.skin_image}">${character_data.skin_image}</option>
                  ${app_state.available_characters_skins.map(
                image_name => `
                      <option value="${image_name}">
                        ${image_name}
                      </option>
                    `
            )}
                </select>
              </div>
            `
            characters_list_elem.innerHTML += new_character_element_raw
        }
    })

    // Remove characters if they no longer exist in the story
    let existing_characters_names = getCharactersNamesInCharactersDetailsList()
    existing_characters_names.forEach(existing_name => {
        if (!app_state.actors.includes(existing_name)) {
            debugger
            document.getElementById(`${CHARACTER_DETAILS_ID_PREFIX}${existing_name}`).remove()

        }
    })
}

let updateParsedStory = () => {
    document.querySelector("#parsed_story").innerHTML = app_state.scenario.map(scenario_elem => {
        return `<div>${scenario_elem.actor}: ${scenario_elem.content}</div>`;
    }).join('');
}

// ============ UPDATE DATA
setInterval(function () {
    eel.get_characters_faces()(function (photos) {
        app_state.available_characters_photos = photos
    })
    eel.get_characters_skins()(function (photos) {
        app_state.available_characters_skins = photos
    })
}, 1001);


// periodically checks the raw scenario textedit and updates parsed story and editable elements
setInterval(function () {
    let scenario_raw = document.getElementById("scenario_raw").value
    let characters_overrides = getCharactersEditToCharactersOverridePayload()

    eel.parse_scenario(
        scenario_raw,
        characters_overrides
    )(function (parsed_data) {
        debugger

        app_state.scenario = parsed_data.parsed_story.scenario
        app_state.actors = parsed_data.parsed_story.actors
        app_state.characters = parsed_data.characters

        updateParsedStory()
        updateCharacters()
    })
}, 1000);

let getCharactersEditToCharactersOverridePayload = () => {
    let characters_override_payload = []

    getCharactersNamesInCharactersDetailsList().forEach(character_name => {
        let character_face_image = document.getElementById(CHARACTER_FACE_SELECT_ID_PREFIX + character_name).value
        let character_skin_image = document.getElementById(CHARACTER_SKIN_SELECT_ID_PREFIX + character_name).value

        characters_override_payload.push({
            name: character_name,
            face_image: character_face_image,
            skin_image: character_skin_image
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
