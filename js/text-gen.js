




for (var i = 1; i < 6; i++){

    var sents = Math.floor((Math.random() * 10) + 1)

    var par = ""

    for (var j = 0; j < sents; j++) {

        index = Math.floor(Math.random() * data.length)
        par += " " + data[index]

    }

    $('section#' + i + ' p').html(par)
}
