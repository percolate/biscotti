
window.addEventListener('load', function () {
    var jsonViewer = new JSONViewer();
    document.querySelector("#json").appendChild(jsonViewer.getContainer());
    jsonViewer.showJSON(JSON.parse(api_data));

});
