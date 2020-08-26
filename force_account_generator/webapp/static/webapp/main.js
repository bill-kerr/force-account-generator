function initDropzone() {
  const previewNode = document.getElementById("dropzone-template");
  previewNode.id = "";
  const previewTemplate = previewNode.parentNode.innerHTML;
  previewNode.parentNode.removeChild(previewNode);

  Dropzone.options.dropzone = {
    maxFiles: 1,
    init: function () {
      this.hiddenFileInput.removeAttribute("multiple");
      this.on("addedfile", onAddedFile);
      this.on("uploadprogress", onUploadProgress);
      this.on("maxfilesexceeded", onMaxFilesExceeded);
    },
    paramName: "docfile",
    createImageThumbnails: false,
    acceptedFiles: ".xlsx",
    previewTemplate: previewTemplate,
    previewsContainer: "#upload-status",
  };
}
initDropzone();

const initialState = {
  uploading: false,
  fileBytes: 0,
  bytesSent: 0,
  fileSizeUnit: "KB",

  setUploading({ fileBytes }) {
    this.uploading = true;
    this.fileBytes = fileBytes;
    this.fileSizeUnit = fileBytes / 1000 >= 1000 ? "MB" : "KB";
  },

  _getSize(bytes) {
    if (this.fileSizeUnit === "KB") {
      return (Math.round((bytes / 1000) * 100) / 100).toFixed(2);
    }
    return (Math.round((bytes / 1000000) * 100) / 100).toFixed(2);
  },

  get fileSize() {
    return this._getSize(this.fileBytes);
  },

  get transferredSize() {
    return Math.min(this._getSize(this.bytesSent), this.fileBytes);
  },

  get transferredPercent() {
    const percent = Math.min((this.bytesSent / this.fileBytes) * 100, 100);
    return percent.toString() + "%";
  },
};

function onAddedFile(file) {
  window.dispatchEvent(new CustomEvent("addedfile", { detail: { fileBytes: file.size } }));
}

function onUploadProgress(_file, progress, bytesSent) {
  window.dispatchEvent(new CustomEvent("uploadprogress", { detail: { progress, bytesSent } }));
}

function onMaxFilesExceeded(file) {
  this.removeAllFiles(true);
  this.addFile(file);
}

var stage1 = document.getElementById("stage-1");
var stage2 = document.getElementById("stage-2");
var stage3 = document.getElementById("stage-3");

function initCeleryProgress(taskId) {
  const progressUrl = "/celery-progress/" + taskId;
  console.log(progressUrl);
  CeleryProgressBar.initProgressBar(progressUrl, {
    onProgress: onProgress,
    onSuccess: onSuccess,
    onError: onError,
  });
}

function onProgress(_progElem, _msgElem, { description: progress }) {
  if (!progress) {
    return;
  }
}

function showAlpine() {
  return false;
}

function onSuccess(_progElem, _msgElem, result) {
  //console.log(result);
}

function onError(_progElem, _msgElem, errorMessage) {
  //console.error(errorMessage);
}

// function setStage(stage) {
//   switch (stage) {
//     case 1:
//       activate(stage1);
//       return;
//     case 2:
//       complete(stage1);
//       activate(stage2);
//       return;
//     case 3:
//       complete(stage1, stage2);
//       activate(stage3);
//       return;
//   }
// }

// function activate(...elements) {
//   elements.forEach((elem) => elem.classList.add("active"));
// }

// function complete(...elements) {
//   elements.forEach((elem) => {
//     elem.classList.add("completed");
//     elem.classList.remove("active");
//   });
// }

// function setProgress(progress, total) {
//   var bar = document.getElementById("progress-bar");
//   var currentElem = document.getElementById("current-page");
//   var totalElem = document.getElementById("total-pages");
//   var percent = (progress / total) * 100;
//   bar.style.width = percent + "%";
//   if (progress !== total) {
//     currentElem.innerHTML = progress;
//     totalElem.innerHTML = total;
//   } else {
//     currentElem.innerHTML = totalElem.innerHTML;
//     bar.style.backgroundColor = "#68d391";
//   }
// }

// function onProgress(_progElem, _messageElem, progress) {
//   console.log(progress);
//   if (!progress.description) {
//     return;
//   }
//   var status = progress.description;

//   setStage(status.stage);

//   if (status.stage === 2) {
//     setProgress(status["stage_progress"], status["stage_total"]);
//   }

//   if (status.stage === 3) {
//     setProgress(1, 1);
//   }
// }

// function onSuccess(_progElem, _messageElem, result) {
//   if (result === true) {
//     complete(stage1, stage2, stage3);
//   }

//   stage2.querySelector(".step-content").style.display = "none";
//   document.getElementById("pdf-download").classList.remove("disabled");
// }

// function onError(_progElem, _messageElem, errorMessage) {
//   console.log("Error:");
//   console.log(errorMessage);
// }
