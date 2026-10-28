let totalScans = 0;
let scamsDetected = 0;
let safeMessages = 0;
let highRisk = 0;


async function detectScam() {

    const message =
        document.getElementById("message").value;


    if (message.trim() === "") {

        alert("Please enter a message.");

        return;
    }


    const response = await fetch("/detect", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: message
        })

    });


    const data = await response.json();
    const riskFill = document.getElementById("riskFill");
    const scoreDisplay = document.getElementById("score");

if (scoreDisplay) {
    scoreDisplay.innerText = data.score;
}

if (riskFill) {
    riskFill.style.width = data.score + "%";

    if (data.score >= 60) {
        riskFill.style.background = "#dc2626";
    }
    else if (data.score >= 30) {
        riskFill.style.background = "#f59e0b";
    }
    else {
        riskFill.style.background = "#16a34a";
    }
}

    console.log("DATA FROM SERVER:", data);

    if (data.error) {

        alert(data.error);

        return;
    }


    totalScans++;

    const scanHistory = JSON.parse(localStorage.getItem("scanHistory")) || [];

scanHistory.push({
    message: message,
    score: data.score,
    risk: data.risk
});

localStorage.setItem("scanHistory", JSON.stringify(scanHistory));


    if (data.score >= 30) {

    scamsDetected++;

}

if (data.score >= 60) {

    highRisk++;

} else if (data.score < 30) {

    safeMessages++;
}


    document.getElementById("totalScans")
        .innerText = totalScans;

    document.getElementById("scamsDetected")
        .innerText = scamsDetected;

    document.getElementById("safeMessages")
        .innerText = safeMessages;

    document.getElementById("highRisk")
        .innerText = highRisk;


    document
        .getElementById("result")
        .classList.remove("hidden");


    document.getElementById("score")
        .innerText = data.score;


    const risk =
        document.getElementById("risk");


    risk.innerText = data.risk;


    risk.className = "risk";


    if (data.score >= 60) {

        risk.classList.add("high");

    } else if (data.score >= 30) {

        risk.classList.add("medium");

    } else {

        risk.classList.add("low");
    }


    const warningList =
        document.getElementById("warnings");


    warningList.innerHTML = "";


    if (data.warnings.length === 0) {

        const li =
            document.createElement("li");

        li.innerText =
            "No suspicious indicators found.";

        warningList.appendChild(li);

    } else {

        data.warnings.forEach(function(warning) {

            const li =
                document.createElement("li");

            li.innerText =
                "⚠️ " + warning;

            warningList.appendChild(li);

        });
    }


    document.getElementById("recommendation")
        .innerText = data.recommendation;
}