// Code taken from https://github.com/codebasics/py/tree/master/DataScience/CelebrityFaceRecognition
Dropzone.autoDiscover = false;

function init() {
    let dz = new Dropzone("#dropzone", {
        url: "/",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });
    
    dz.on("addedfile", function() {
        if (dz.files[1]!=null) {
            dz.removeFile(dz.files[0]);        
        }
    });

    dz.on("complete", function (file) {
        let imageData = file.dataURL;
        
        var url = "http://127.0.0.1:5000/classify";

        $.post(url, {
            image_data: file.dataURL
        },function(data, status) {
            console.log(data);
            if (!data || data.length==0) {
                $("#resultHolder").hide();
                $("#divClassTable").hide();                
                $("#error").show();
                return;
            }
            let leaders = ["narendra modi", "joe biden", "justin trudeau", "vladimir putin", "xi jinping"];
            
            let match = null;
            let bestScore = -1;
            for (let i=0;i<data.length;++i) {
                let maxScoreForThisClass = Math.max(...data[i].class_probability);
                if(maxScoreForThisClass>bestScore) {
                    match = data[i];
                    bestScore = maxScoreForThisClass;
                }
            }
            if (match) {
                $("#error").hide();
                $("#resultHolder").show();
                $("#divClassTable").show();
                $("#resultHolder").html($(`[data-leader="${match.class}"`).html());
                let classDictionary = match.class_dictionary;
                for(let leaderName in classDictionary) {
                    let index = classDictionary[leaderName];
                    let proabilityScore = match.class_probability[index];
                    console.log(leaderName, proabilityScore);
                    for (let i=0;i<leaderName.length;++i) {
                        if (leaderName[i]==' ') {
                            leaderName = leaderName.slice(0, i) + '_' + leaderName.slice(i+1, leaderName.length);
                        }
                    }
                    let elementName = "#score_" + leaderName;
                    $(elementName).html(proabilityScore);
                }
            }          
        });
    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();		
    });
}

$(document).ready(function() {
    console.log( "ready!" );
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();

    init();
});