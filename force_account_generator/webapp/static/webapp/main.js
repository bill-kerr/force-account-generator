function initDropzone() {
  const previewNode = document.getElementById("dropzone-template");
  previewNode.id = "";
  const previewTemplate = previewNode.parentNode.innerHTML;
  previewNode.parentNode.removeChild(previewNode);

  Dropzone.options.dropzone = {
    maxFiles: 1,
    init: function () {
      this.hiddenFileInput.removeAttribute("multiple");
      this.on("processing", onProcessing);
      this.on("uploadprogress", onUploadProgress);
      this.on("maxfilesexceeded", onMaxFilesExceeded);
      this.on("success", onUploadSuccess);
      this.on("sending", onSending);
      this.on("error", onUploadError);
    },
    paramName: "docfile",
    createImageThumbnails: false,
    acceptedFiles: ".xlsx",
    previewTemplate: previewTemplate,
    previewsContainer: "#upload-status",
  };
}
initDropzone();

const appData = {
  fileAdded: false,
  uploading: false,
  fileBytes: 0,
  bytesSent: 0,
  fileSizeUnit: "KB",
  error: null,
  stage: 0,
  currentPage: 0,
  totalPages: 0,
  taskId: null,

  get fileSize() {
    return this._getSize(this.fileBytes);
  },

  get transferredSize() {
    return this._getSize(Math.min(this.bytesSent, this.fileBytes));
  },

  get transferredPercent() {
    const percent = Math.min((this.bytesSent / this.fileBytes) * 100, 100);
    return percent.toString() + "%";
  },

  _getSize(bytes) {
    if (this.fileSizeUnit === "KB") {
      return (Math.round((bytes / 1000) * 100) / 100).toFixed(2);
    }
    return (Math.round((bytes / 1000000) * 100) / 100).toFixed(2);
  },

  reset() {
    this.error = null;
    this.fileAdded = false;
    this.uploading = false;
    this.fileBytes = 0;
    this.bytesSent = 0;
    this.fileSizeUnit = "KB";
    this.stage = 0;
    this.currentPage = 0;
    this.totalPages = 0;
    this.taskId = null;
  },

  setUploading({ fileBytes }) {
    this.fileAdded = true;
    this.uploading = true;
    this.error = null;
    this.fileBytes = fileBytes;
    this.fileSizeUnit = fileBytes / 1000 >= 1000 ? "MB" : "KB";
  },

  setStage(stage) {
    this.stage = stage;
    if (this.stage >= 3 && this.currentPage !== this.totalPages) {
      this.currentPage = this.totalPages;
    }
  },
};

function onProcessing(file) {
  window.dispatchEvent(new CustomEvent("processingupload", { detail: { fileBytes: file.size } }));
}

function onUploadProgress(_file, progress, bytesSent) {
  window.dispatchEvent(new CustomEvent("uploadprogress", { detail: { progress, bytesSent } }));
}

function onUploadSuccess(_file, response) {
  if (response["task_id"]) {
    window.dispatchEvent(new CustomEvent("uploadsuccess", { detail: { taskId: response["task_id"] } }));
    return initCeleryProgress(response["task_id"]);
  }
  dispatchError("No response from the server. Please try again in a little bit.");
}

function onUploadError(_file, errorMessage) {
  this.removeAllFiles(true);
  dispatchError(errorMessage);
}

function onMaxFilesExceeded(file) {
  this.removeAllFiles(true);
  this.addFile(file);
}

function onSending(_file, _xhrObj, formData) {
  const dailySheets = document.getElementById("daily_sheets").checked;
  formData.append("daily_sheets", dailySheets);
}

function initCeleryProgress(taskId) {
  const progressUrl = "/celery-progress/" + taskId;
  CeleryProgressBar.initProgressBar(progressUrl, {
    onProgress: onGenerateProgress,
    onSuccess: onGenerateSuccess,
    onError: onGenerateError,
  });
}

function onGenerateProgress(_progElem, _msgElem, { description: progress }) {
  if (!progress) {
    return;
  }
  dispatchSetStage(progress.stage);

  if (progress.stage === 2) {
    const current = progress["stage_progress"];
    const total = progress["stage_total"];
    window.dispatchEvent(new CustomEvent("pdfprogress", { detail: { current, total } }));
  }
}

function onGenerateSuccess(_progElem, _msgElem, _result) {
  dispatchSetStage(4);
}

function onGenerateError(_progElem, _msgElem, _errorMessage) {
  dispatchError("An error occurred while processing the Excel file. Please make sure it is a valid template.");
}

function dispatchError(errorMessage) {
  window.dispatchEvent(new CustomEvent("error", { detail: { error: errorMessage } }));
}

function dispatchSetStage(stage) {
  window.dispatchEvent(new CustomEvent("setstage", { detail: { stage } }));
}
