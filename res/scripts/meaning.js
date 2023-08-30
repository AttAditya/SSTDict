async function load_meanings(item) {
    await fetch(`/meaning/${item}/get`).then(req => req.json()).then(data => {
        if (!data.OK) { return }

        console.log(data);

        let examples_container = document.getElementById("examples-container");
        let alternatives_container = document.getElementById("alternatives-container");
        let emotions_container = document.getElementById("emotions-container");
        let tags_container = document.getElementById("tags-container");
        
        examples_container.innerHTML = "";
        alternatives_container.innerHTML = "";
        emotions_container.innerHTML = "";
        tags_container.innerHTML = "";

        for (let tag of data.tags) {
            tags_container.innerHTML += `<span class="tag is-medium is-info">${tag}</span>`;
        }

        if (!data.examples.length) {
            tags_container.innerHTML = "No tags here!";
        }

        for (let example of data.examples) {
            examples_container.innerHTML += `<blockquote>${example}</blockquote>`;
        }

        if (!data.examples.length) {
            examples_container.innerHTML = "No examples here!";
        }

        for (let alternative of data.alternatives) {
            alternatives_container.innerHTML += `
                <div class="column is-4">
                    <div class="box has-background-info has-text-white">
                        <div class="title has-text-white mb-2">
                            ${alternative.word}
                        </div>
                        <div class="subtitle has-text-white mt-2 is-italic">
                            ${alternative.usage}
                        </div>
                    </div>
                </div>
            `;
        }

        if (!data.alternatives.length) {
            alternatives_container.innerHTML = `
                <div class="column is-4">
                    <div class="box has-background-info has-text-white">
                        <div class="title has-text-white mb-2">
                            ${item}
                        </div>
                        <div class="subtitle has-text-white mt-2 is-italic">
                            Really? You need a better alternative for "${item}"?
                        </div>
                    </div>
                </div>
            `;
        }

        for (let emotion of Object.keys(data.emos)) {
            let emotion_value = data.emos[emotion];

            emotions_container.innerHTML += `
                <div class="title is-size-5 is-capitalized has-text-weight-bold has-text-white mb-2">
                    ${emotion} (${emotion_value * 100}%)
                </div>
                <progress class="progress is-black" value="${emotion_value}" max="1"></progress>
            `;
        }
    }).catch(err => {
        load_meanings(item);
    });
}