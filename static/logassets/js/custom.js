

$(".symptomOut").click(function () {
    console.log("clicked")
    fullDivId = $(this).attr('id');
    console.log(fullDivId);
    peerId = fullDivId.substring(fullDivId.indexOf("-") + 1);
    lineId = "online-" + peerId ;
    var postly = document.getElementById(peerId);
    console.log(postly);
    if (postly.value == 'on') {
        document.getElementById(lineId).style.display = "none";
        postly.value = 'off'
    }
    else{
        document.getElementById(lineId).style.display = "block";
        postly.value = 'on'
    }
});

