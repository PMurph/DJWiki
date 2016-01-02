describe('FormUtilities', function() {
        describe('formToJson', function() {
        var firstNamedElement;
        var secondNamedElement;
        var nonNamedElement;
        
        beforeEach(function() {
            firstNamedElement = {'getAttribute': function() {}};
            spyOn(firstNamedElement, 'getAttribute').and.returnValue('first');
            firstNamedElement.value = '1st'
            
            secondNamedElement = {'getAttribute': function() {}};
            spyOn(secondNamedElement, 'getAttribute').and.returnValue('second');
            secondNamedElement.value = '2nd';
            
            nonNamedElement = {'getAttribute': function() {}}
            spyOn(nonNamedElement, 'getAttribute').and.returnValue(null);
        });
        
        afterEach(function() {
            expect(firstNamedElement.getAttribute).toHaveBeenCalledWith('name');
            expect(secondNamedElement.getAttribute).toHaveBeenCalledWith('name');
        });
        
        it('should create a json object with form element names to values', function() {
            var form = {'elements': {0: firstNamedElement, 1: secondNamedElement, 'length': 2}};
            
            formJson = formToJson(form);
            
            expect(formJson).toEqual('{"first":"1st","second":"2nd"}');
        });
        
        it('should not contain the value of a form element with no name', function() {
            var form = {'elements': {0: firstNamedElement, 1: secondNamedElement, 2: nonNamedElement, 'length': 3}};
            
            formJson = formToJson(form);
            
            expect(formJson).toEqual('{"first":"1st","second":"2nd"}');
            expect(nonNamedElement.getAttribute).toHaveBeenCalledWith('name');
        });
    });
});