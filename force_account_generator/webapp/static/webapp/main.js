var stage1 = document.getElementById("stage-1");
var stage2 = document.getElementById("stage-2");
var stage3 = document.getElementById("stage-3");

function setStage(stage) {
  switch (stage) {
    case 1:
      activate(stage1);
      return;
    case 2:
      complete(stage1);
      activate(stage2);
      return;
    case 3:
      complete(stage1, stage2);
      activate(stage3);
      return;
  }
}

function activate(...elements) {
  elements.forEach((elem) => elem.classList.add("active"));
}

function complete(...elements) {
  elements.forEach((elem) => {
    elem.classList.add("completed");
    elem.classList.remove("active");
  });
}

function setProgress(progress, total) {
  var bar = document.getElementById("progress-bar");
  var currentElem = document.getElementById("current-page");
  var totalElem = document.getElementById("total-pages");
  var percent = (progress / total) * 100;
  bar.style.width = percent + "%";
  if (progress !== total) {
    currentElem.innerHTML = progress;
    totalElem.innerHTML = total;
  } else {
    currentElem.innerHTML = totalElem.innerHTML;
    bar.style.backgroundColor = "#68d391";
  }
}

function onProgress(_progElem, _messageElem, progress) {
  console.log(progress);
  if (!progress.description) {
    return;
  }
  var status = progress.description;

  setStage(status.stage);

  if (status.stage === 2) {
    setProgress(status["stage_progress"], status["stage_total"]);
  }

  if (status.stage === 3) {
    setProgress(1, 1);
  }
}

function onSuccess(_progElem, _messageElem, result) {
  if (result === true) {
    complete(stage1, stage2, stage3);
  }

  stage2.querySelector(".step-content").style.display = "none";
  document.getElementById("pdf-download").classList.remove("disabled");
}

function onError(_progElem, _messageElem, errorMessage) {
  console.log("Error:");
  console.log(errorMessage);
}
