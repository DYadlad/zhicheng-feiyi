document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const selectFileBtn = document.getElementById('selectFileBtn');
    const previewArea = document.getElementById('previewArea');
    const originalImage = document.getElementById('originalImage');
    const originalInfo = document.getElementById('originalInfo');
    const restoredImage = document.getElementById('restoredImage');
    const restoredContainer = document.getElementById('restoredContainer');
    const restoredPlaceholder = document.getElementById('restoredPlaceholder');
    const restoredInfo = document.getElementById('restoredInfo');
    const restoreBtn = document.getElementById('restoreBtn');
    const reuploadBtn = document.getElementById('reuploadBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const progressArea = document.getElementById('progressArea');
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');

    let currentFilename = null;
    let restoredFilename = null;

    selectFileBtn.addEventListener('click', function() {
        fileInput.click();
    });

    uploadArea.addEventListener('click', function(e) {
        if (e.target !== selectFileBtn) {
            fileInput.click();
        }
    });

    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.style.background = '#f0f0f0';
    });

    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.style.background = '';
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.style.background = '';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            handleFile(file);
        }
    });

    async function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('请上传图片文件！');
            return;
        }

        if (file.size > 16 * 1024 * 1024) {
            alert('文件大小不能超过16MB！');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                currentFilename = result.filename;
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    originalImage.src = e.target.result;
                    originalInfo.textContent = `文件名: ${file.name} | 大小: ${(file.size / 1024).toFixed(2)} KB`;
                    
                    uploadArea.style.display = 'none';
                    previewArea.style.display = 'block';
                    restoreBtn.disabled = false;
                    
                    resetRestoredImage();
                };
                reader.readAsDataURL(file);
            } else {
                alert(result.error || '上传失败！');
            }
        } catch (error) {
            console.error('上传失败:', error);
            alert('上传失败，请稍后重试！');
        }
    }

    function resetRestoredImage() {
        restoredImage.style.display = 'none';
        restoredImage.src = '';
        restoredPlaceholder.style.display = 'block';
        restoredPlaceholder.innerHTML = '<p>等待修复...</p>';
        restoredInfo.textContent = '';
        downloadBtn.style.display = 'none';
        restoredFilename = null;
    }

    restoreBtn.addEventListener('click', async function() {
        if (!currentFilename) {
            alert('请先上传图片！');
            return;
        }

        restoreBtn.disabled = true;
        progressArea.style.display = 'block';
        progressText.textContent = '正在修复图片，请稍候...';

        try {
            const response = await fetch('/api/restore', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    filename: currentFilename
                })
            });

            const result = await response.json();

            if (result.success) {
                restoredFilename = result.restored_filename;
                
                restoredImage.src = `/uploads/${restoredFilename}`;
                restoredImage.style.display = 'block';
                restoredPlaceholder.style.display = 'none';
                restoredInfo.textContent = '修复完成！';
                downloadBtn.style.display = 'inline-block';
                
                progressText.textContent = '修复完成！';
            } else {
                alert(result.error || '修复失败！');
                progressText.textContent = '修复失败！';
            }
        } catch (error) {
            console.error('修复失败:', error);
            alert('修复失败，请稍后重试！');
            progressText.textContent = '修复失败！';
        } finally {
            restoreBtn.disabled = false;
            setTimeout(() => {
                progressArea.style.display = 'none';
            }, 2000);
        }
    });

    reuploadBtn.addEventListener('click', function() {
        uploadArea.style.display = 'block';
        previewArea.style.display = 'none';
        fileInput.value = '';
        currentFilename = null;
        resetRestoredImage();
    });

    downloadBtn.addEventListener('click', function() {
        if (restoredFilename) {
            const link = document.createElement('a');
            link.href = `/uploads/${restoredFilename}`;
            link.download = restoredFilename;
            link.click();
        }
    });
});
