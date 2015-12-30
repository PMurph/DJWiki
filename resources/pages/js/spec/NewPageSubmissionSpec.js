describe("New Wiki Page Form Submission", function() {
    describe('createNewPage', function() {
        it('should make a asynchronous ajax post requests with a JSON object', function() {
            var xmlHttpRequestSpy = jasmine.createSpyObj('XMLHttpRequest', ['send', 'open', 'setRequestHeader']);
            var formJson = '{"first":"1st","second":"2nd"}';
            
            createNewPage(formJson, xmlHttpRequestSpy, null);
            
            expect(xmlHttpRequestSpy.open).toHaveBeenCalledWith('POST', '../create/', true);
            expect(xmlHttpRequestSpy.setRequestHeader).toHaveBeenCalledWith('Content-Type', 'application/json');
            expect(xmlHttpRequestSpy.send).toHaveBeenCalledWith(formJson);
            expect(xmlHttpRequestSpy.onreadystatechange).toBeTruthy();
        });
    });
    
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
    
    describe('handleCreatePageResponse', function() {
        var windowMock;
        var currPage;
        var baseURIl
        var wikiPage;
        
        beforeEach(function() {
            baseURI = "http://www.test.com/pages/"
            wikiPage = "NewPage";
            currPage = baseURI + 'new' ;
            windowMock = { 'location': { 'href': currPage } };
        });
        
        it('should redirect if response successfully creates page and curr page URL contains terminating slash', function() {
            var xmlHttpRequestMock = { 'readyState': 4, 'status': 200, 'responseText': '{"wikiPage":"' + wikiPage + '"}'};
            windowMock.location.href = windowMock.location.href+ "/"
            
            handleCreatePageResponse(xmlHttpRequestMock, windowMock);
            
            expect(windowMock.location).toEqual(baseURI + wikiPage);
        });
        
        it('should redirect if response successfully creates page and curr page URL does not contain terminating slash', function() {
            var xmlHttpRequestMock = { 'readyState': 4, 'status': 200, 'responseText': '{"wikiPage":"' + wikiPage + '"}'};
            
            handleCreatePageResponse(xmlHttpRequestMock, windowMock);
            
            expect(windowMock.location).toEqual(baseURI + wikiPage);
        });
        
        it('should not redirect if response contains errors', function() {
            var xmlHttpRequestMock = { 'readyState': 4, 'status': 200, 'responseText': '{"errors": ["test1", "test2"]}' };
            
            handleCreatePageResponse(xmlHttpRequestMock, windowMock);
            
            expect(windowMock.location.href).toEqual(currPage);
        });
        
        it('should not redirect if the response status is not 200', function() {
            var xmlHttpRequestMock = { 'readyState': 4, 'status': 404, 'responseText': '{"wikiPage":"' + wikiPage + '"}'};
            
            handleCreatePageResponse(xmlHttpRequestMock, windowMock);
            
            expect(windowMock.location.href).toEqual(currPage);
        });
        
        it('should not redirect if the readyState is not 4', function() {
            var xmlHttpRequestMock = { 'readyState': 3, 'status': 200, 'responseText': '{"wikiPage":"' + wikiPage + '"}'};
            
            handleCreatePageResponse(xmlHttpRequestMock, windowMock);
            
            expect(windowMock.location.href).toEqual(currPage);
        });
    });
});
