function deletePage(form_json, xml_http_request, window) {
    xml_http_request.onreadystatechange = function() {
        handleDeletePageResponse(xml_http_request, window);
    }
    xml_http_request.open('POST', 'delete/', true);
    xml_http_request.setRequestHeader('Content-Type', 'application/json');
    xml_http_request.send(form_json);
}

function handleDeletePageResponse(xml_http_request, window) {
    if(xml_http_request.readyState === 4) {
        if(xml_http_request.status === 200) {
            ajaxResponse = JSON.parse(xml_http_request.responseText);
            if(!("errors" in ajaxResponse)) {
                // Have to handle both the situation where the current page URL ends in / and when it does not end in a slash
                if(window.location.href[window.location.href.length-1] == "/") {
                    window.location = new URL(window.location.href + "../new/").toString();
                } else {
                    window.location = new URL(window.location.href + "/../new/").toString();
                }
            }
        }
    }
}