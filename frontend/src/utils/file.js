function forceFileDownload(response) {
    const filename = filename_from_response(response);
    const url = window.URL.createObjectURL(new Blob([response.data], { type: response.headers['content-type'] }));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
}

function filename_from_response(response) {
    return response.headers['content-disposition'].split('filename=')[1].split(';')[0].replaceAll('"', '');
}

export default forceFileDownload;
