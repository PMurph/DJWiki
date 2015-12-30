function createNewPage(formJson, xml_http_request, window) {
    xml_http_request.onreadystatechange = function() {
        handleCreatePageResponse(xml_http_request, window);
    }
    xml_http_request.open('POST', '../create/', true);
    xml_http_request.setRequestHeader('Content-Type', 'application/json');
    xml_http_request.send(formJson);
}

function formToJson(form) {
    var formValues = {}
    
    for(var i =0; i < form.elements.length; i++) {
        var elementName = form.elements[i].getAttribute('name');
        if(elementName !== null) {
            formValues[elementName] = form.elements[i].value;
        }
    }
    
    return JSON.stringify(formValues);
}

function handleCreatePageResponse(xml_http_request, window) {
    if(xml_http_request.readyState === 4) {
        if(xml_http_request.status === 200) {
            ajaxResponse = JSON.parse(xml_http_request.responseText);
            if(ajaxResponse.wikiPage) {
                // Have to handle both the situation where the current page URL ends in / and when it does not end in a slash
                if(window.location.href[window.location.href.length-1] == "/") {
                    window.location = new URL(window.location.href + "../" + ajaxResponse.wikiPage).toString();
                } else {
                    window.location = new URL(window.location.href + "/../" +  ajaxResponse.wikiPage).toString();
                }
            }
        }
    }
}