async function search(query, output) {
    if (!query) {
        output.innerHTML = "";
        output.classList.add("is-hidden");
        return;
    }

    await fetch(`/search/${query}`).then(req => req.json()).then(data => {
        output.innerHTML = "";

        for (let word_data of data.sort()) {
            output.innerHTML += `
                <a href="/meaning/${word_data[1]}" class="button is-outlined is-info column is-full my-1">
                    ${word_data[1]}
                </a>
            `;
        }

        output.classList.remove("is-hidden");
    }).catch(err => {
        load_meanings(item);
    });
}