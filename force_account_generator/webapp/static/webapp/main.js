function onProgress(_progElem, _messageElem, progress) {
  console.log(progress);
  if (!progress.description || !progress.description.progress) {
    return;
  }
}

function onSuccess(_progElem, _messageElem, result) {
  console.log("Success result:");
  console.log(result);
}

function onError(_progElem, _messageElem, errorMessage) {
  console.log("Error:");
  console.log(errorMessage);
}
