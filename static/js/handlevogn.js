var oppdaterKnp = document.getElementsByClassName('oppdater');

for (i = 0; i < oppdaterKnp.length; i++) {
    oppdaterKnp[i].addEventListener("click", function () {

        produktId = this.dataset.produkt;
        handling = this.dataset.handling;

        console.log('Bruker:', bruker)
        if (bruker == "AnonymousUser") {
            gjestBruker(produktId, handling)
        } else {
            oppdaterHandlevogn(produktId, handling)
        }
    })

}

function gjestBruker(produktId, handling) {
    console.log(produktId, handling)
    console.log("Bruker ikke logget inn")

    if (handling == 'adder') {
        if (handlevogn[produktId] == undefined) {
            handlevogn[produktId] = { 'antall': 1 };
        } else {
            handlevogn[produktId]['antall'] += 1;
        }
    }

    if (handling == 'trekk') {

        handlevogn[produktId]['antall'] -= 1;

        if (handlevogn[produktId]['antall'] == 0) {
            handlevogn[produktId]['antall'] = 1
        }
    }

    if (handling == 'slett'){
        delete handlevogn[produktId]
    }

    document.cookie = "handlevogn=" + JSON.stringify(handlevogn) + ";domain=;path=/"
    console.log(handlevogn)
    location.reload()
}

function oppdaterHandlevogn(produktId, handling) {
    console.log('Bruker er logget inn')
    console.log('Id: ', produktId, 'Handling: ', handling)

    var url = '/oppdater/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(
            {
                'produktId': produktId,
                'handling': handling,
            })
    }).then((response) => {
        return response.json();
    }).then((data) => {
        location.reload();
    });

}

