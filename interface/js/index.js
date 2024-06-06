let filenameBefore = '';
let filenameAfter = '';
var HOST = 'localhost:8000';

document.querySelectorAll('.dropzone').forEach(function(dropzone) {
    dropzone.addEventListener('dragover', function(event) {
        event.preventDefault();
        event.stopPropagation();
    });
});
Dropzone.autoDiscover = false;

function createDropzoneConfig(keyValue) {
    return {
        url: `http://${HOST}/upload`,
        uploadMultiple: false,
        maxFiles: 1,
        addRemoveLinks: true,
        params: {
            key: keyValue 
        },
        init: function() {
            this.on("removedfile", function(file) {
                var formData = new FormData();
                formData.append('filename', file.name); 
                fetch(`http://${HOST}/delete`, {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Delete response:', data);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
            });
        }
    };
}
var myDropzone = new Dropzone("#before-upload", createDropzoneConfig());

document.getElementById('startprocesingbtn').addEventListener('click', function() {
    var downloadButton = document.getElementById('DownloadFileButton');
    downloadButton.style.visibility = "visible";
    downloadButton.disabled = true;
    downloadButton.textContent = 'Cравнение...'; 
    downloadButton.classList.remove('btn-success', 'btn-danger', 'btn-warning');
    downloadButton.classList.add('btn-warning'); 
    

    fetch(`http://${HOST}/process`, {
        method: 'POST'
    })
    .then(response => {
        console.log(HOST)
        if (response.ok) {
            return response.json(); 
        } else {
            throw new Error('Failed to process file');
        }
    })
    .then(data => {
        console.log('Process response:', data);
        downloadButton.disabled = false;
        downloadButton.textContent = 'Скачать итоговый документ в папку "загрузки"';
        downloadButton.classList.remove('btn-success', 'btn-danger', 'btn-warning');
        downloadButton.classList.add('btn-success');
        
    })
    .catch((error) => {
        console.error('Error:', error);
        downloadButton.textContent = 'Ошибка сравнения'; 
        downloadButton.classList.remove('btn-success', 'btn-danger', 'btn-warning');
        downloadButton.classList.add('btn-danger'); 
        
    });
});
