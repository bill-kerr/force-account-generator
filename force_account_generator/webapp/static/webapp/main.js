function onProgress(_progElem, _messageElem, progress) {
  console.log(progress);
  if (!progress.description || !progress.description.progress) {
    return;
  }
  var status = progress.description;
  var stage1 = document.getElementById("stage-1");
  var stage2 = document.getElementById("stage-2");
  var stage3 = document.getElementById("stage-3");

  console.log(status.stage);

  var width = (progress.description.progress * 100).toString() + "%";
  document.getElementById("pdf-page-progress").style.width = width;
}

function onSuccess(_progElem, _messageElem, result) {
  console.log("Success result:");
  console.log(result);
}

function onError(_progElem, _messageElem, errorMessage) {
  console.log("Error:");
  console.log(errorMessage);
}
