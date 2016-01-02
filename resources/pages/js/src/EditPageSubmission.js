function updatePage(form_json, xml_http_request, window) {
    xml_http_request.onreadystatechange = function() {
        handleUpdatePageResponse(xml_http_request, window);
    }
    xml_http_request.open('POST', '../update/', true);
    xml_http_request.setRequestHeader('Content-Type', 'application/json');
    xml_http_request.send(form_json);
}

function handleUpdatePageResponse(xml_http_request, window) {
    if(xml_http_request.readyState === 4) {
        if(xml_http_request.status === 200) {
            ajaxResponse = JSON.parse(xml_http_request.responseText);
            if(ajaxResponse.wikiPage) {
                // Have to handle both the situation where the current page URL ends in / and when it does not end in a slash
                if(window.location.href[window.location.href.length-1] == "/") {
                    window.location = new URL(window.location.href + "../").toString();
                } else {
                    window.location = new URL(window.location.href + "/../").toString();
                }
            }
        }
    }
}