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
