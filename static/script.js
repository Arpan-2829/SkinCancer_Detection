// =====================================
// Capture Scan
// =====================================

function captureScan() {

    fetch("/capture")

    .then(response => response.json())

    .then(data => {

        if (data.status === "error") {

            showToast(
                "Camera Not Ready",
                "danger"
            );

            return;
        }

        // Update prediction text
        document.getElementById(
            "predictionResult"
        ).innerHTML = data.result;


        // Update confidence text
        document.getElementById(
            "confidenceText"
        ).innerHTML =
        data.confidence + "%";


        // Update progress bar
        document.getElementById(
            "confidenceBar"
        ).style.width =
        data.confidence + "%";


        // Color according to prediction

        if (data.result === "BENIGN") {

            document.getElementById(
                "predictionResult"
            ).style.color =
            "#22c55e";

        }

        else {

            document.getElementById(
                "predictionResult"
            ).style.color =
            "#ef4444";


            playAlertSound();

        }


        showToast(
            "Scan Completed Successfully",
            "success"
        );


        loadHistory();

        loadStatistics();

    });

}



// =====================================
// Download Report
// =====================================

function downloadReport() {

    window.location.href =
    "/download_report";

}



// =====================================
// Fullscreen Video
// =====================================

function fullscreenVideo() {

    let video =
    document.getElementById(
        "video"
    );

    if (video.requestFullscreen) {

        video.requestFullscreen();

    }

}



// =====================================
// Toast Notification
// =====================================

function showToast(message, type) {

    let toast =
    document.getElementById(
        "toast"
    );

    toast.innerHTML =

    `
    <div class="alert alert-${type}">
        ${message}
    </div>
    `;


    setTimeout(() => {

        toast.innerHTML = "";

    }, 3000);

}



// =====================================
// Load Statistics
// =====================================

function loadStatistics() {

    fetch("/stats")

    .then(response => response.json())

    .then(data => {

        document.getElementById(
            "totalScans"
        ).innerHTML =
        data.total;


        document.getElementById(
            "benignCount"
        ).innerHTML =
        data.benign;


        document.getElementById(
            "malignantCount"
        ).innerHTML =
        data.malignant;

    });

}



// =====================================
// Load History
// =====================================

function loadHistory() {

    fetch("/history")

    .then(response => response.json())

    .then(data => {

        let cards = "";

        data.forEach(item => {

            let color =

            item.result === "BENIGN"

            ?

            "#22c55e"

            :

            "#ef4444";


            cards +=

            `
            <div class="col-lg-3 mb-4">

            <div class="history-card">

            <img
            src="/static/captures/${item.image}"
            class="history-image">

            <h5
            class="mt-3"
            style="color:${color};">

            ${item.result}

            </h5>

            <p>

            Confidence :
            ${item.confidence}%

            </p>

            <small>

            ${item.time}

            </small>

            </div>

            </div>
            `;

        });


        document.getElementById(
            "historyCards"
        ).innerHTML = cards;

    });

}



// =====================================
// Malignant Sound Alert
// =====================================

function playAlertSound() {

    let audio = new Audio(

    "https://actions.google.com/sounds/v1/alarms/beep_short.ogg"

    );

    audio.play();

}



// =====================================
// Auto Refresh Statistics
// =====================================

setInterval(() => {

    loadStatistics();

}, 5000);



// =====================================
// Initial Load
// =====================================

window.onload = () => {

    loadStatistics();

    loadHistory();

};