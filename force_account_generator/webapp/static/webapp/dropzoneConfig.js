const dropzone = document.getElementById("dropzone");
const previewNode = document.getElementById("dropzone-template");
previewNode.id = "";
const previewTemplate = previewNode.parentNode.innerHTML;
previewNode.parentNode.removeChild(previewNode);

Dropzone.options.dropzone = {
  maxFiles: 1,
  init: function () {
    this.hiddenFileInput.removeAttribute("multiple");

    this.on("addedfile", onAddedFile);
    this.on("error", onError);
    this.on("maxfilesexceeded", onMaxFilesExceeded);
    this.on("uploadprogress", onProgress);
    this.on("processing", onProcessing);
    this.on("success", onSuccess);
  },
  paramName: "docfile",
  createImageThumbnails: false,
  acceptedFiles: ".xlsx",
  previewTemplate: previewTemplate,
  previewsContainer: "#upload-status",
};

function getSize(file, bytesSent = null, showUnit = true) {
  const factor = file.size / 1000 >= 1000 ? 1000000 : 1000;
  const unit = file.size / 1000 >= 1000 ? "MB" : "KB";

  if (bytesSent && bytesSent > file.size) {
    bytesSent = file.size;
  }

  return bytesSent ? convert(bytesSent, factor, unit, showUnit) : convert(file.size, factor, unit, showUnit);
}

function convert(bytes, divisor, unit, showUnit = true) {
  const unitString = showUnit ? " " + unit : "";
  return (Math.round((bytes / divisor) * 100) / 100).toFixed(2).toString() + unitString;
}

function onAddedFile(file) {
  document.getElementById("total-size").innerHTML = getSize(file);
}

function onError(_file, errorMessage) {
  resetDropzone(this);
  console.log(errorMessage);
  dropzone.style.borderColor = "#e53e3e";
  const errorElem = document.getElementById("upload-error");
  errorElem.style.display = "flex";
  errorElem.querySelector("span").innerHTML = errorMessage;
  setTimeout(() => {
    errorElem.style.display = "none";
    dropzone.style.borderColor = "#90cdf4";
  }, 4000);
  return;
}

function resetDropzone(dz) {
  dz.removeAllFiles();
  const messageContainer = dropzone.querySelector(".dropzone-message");
  messageContainer.style.display = "flex";
  dropzone.style.height = "16rem";
  dropzone.style.pointerEvents = "all";
  dropzone.style.border = "3px dashed #90cdf4";
}

function onMaxFilesExceeded(file) {
  this.removeAllFiles(true);
  this.addFile(file);
}

function onProgress(file, progress, bytesSent) {
  const progressElem = document.querySelector("#upload-progress > div");
  progressElem.style.width = progress + "%";
  document.getElementById("transferred-size").innerHTML = getSize(file, bytesSent, false);
}

function onProcessing(_file) {
  dropzone.querySelector(".dropzone-message").style.display = "none";
  dropzone.style.height = "0";
  dropzone.style.pointerEvents = "none";
  dropzone.style.border = "none";
}

function onSuccess(_file, response) {
  const progressElem = document.querySelector("#upload-progress > div");
  progressElem.style.backgroundColor = "#68d391";
  const messageElem = document.querySelector(".dropzone-template-wrapper span");
  messageElem.style.color = "#38A169";
  messageElem.innerHTML = "Uploaded";

  const generateForm = document.getElementById("generate-form");
  generateForm.style.display = "flex";

  const fileIdField = document.getElementById("generate-file-id-field");
  fileIdField.value = response["file_id"];
  console.log(response);
}
