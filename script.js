window.onload = function () {
    loadFiles();
};
function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    if (fileInput.files.length === 0) {
        alert("Please choose a file");
        return;
    }
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);
    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("status").innerHTML = data.message;
        fileInput.value = "";
        loadFiles();
    })
    .catch(error => {
        console.log(error);
    });
}
function loadFiles() {
    fetch("/files")
    .then(response => response.json())
    .then(files => {
        const gallery = document.getElementById("gallery");
        gallery.innerHTML = "<h2>Uploaded Documents</h2>";
        files.forEach(file => {
            gallery.innerHTML += `
            <div class="card">
                <div>
                    📄 ${file.name}
                    <br>
                    <small>${file.size} KB</small>
                </div>
                <div>
                    <button onclick="downloadFile('${file.name}')">
                        Download
                    </button>
                    <button onclick="deleteFile('${file.name}')">
                        Delete
                    </button>
                </div>
            </div>
            `;
        });
    });
}
function downloadFile(filename){
    window.location.href="/download/"+filename;
}
function deleteFile(filename){
    fetch("/delete/"+filename,{
        method:"DELETE"
    })
    .then(response=>response.json())
    .then(data=>{
        alert(data.message);
        loadFiles();
    });
}