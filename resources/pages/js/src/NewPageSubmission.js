function createNewPage(formJson, xml_http_request) {
    
}

function formToJson(form) {
    var formValues = {}
    
    for(var element in form) {
        var elementName = form[element].getAttribute('name');
        if(elementName !== null) {
            formValues[elementName] = form[element].value;
        }
    }
    
    return JSON.stringify(formValues);
}

function handleCreatePageResponse(xml_http_request) {
}