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