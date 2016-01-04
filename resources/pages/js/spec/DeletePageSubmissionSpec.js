describe("Delete Wiki Page Submission", function() {
    describe("deletePage", function() {
        it('should make a asynchronous ajax post requests with a JSON object', function() {
            var xmlHttpRequestSpy = jasmine.createSpyObj('XMLHttpRequest', ['send', 'open', 'setRequestHeader']);
            var formJson = '{"first":"1st","second":"2nd"}';
            
            deletePage(formJson, xmlHttpRequestSpy, null);
            
            expect(xmlHttpRequestSpy.open).toHaveBeenCalledWith('POST', 'delete/', true);
            expect(xmlHttpRequestSpy.setRequestHeader).toHaveBeenCalledWith('Content-Type', 'application/json');
            expect(xmlHttpRequestSpy.send).toHaveBeenCalledWith(formJson);
            expect(xmlHttpRequestSpy.onreadystatechange).toBeTruthy();
        });
    });
    
    describe("handleDeletePageResponse", function() {
        var windowMock;
        var currPage;
        var baseURIl
        var wikiPage;
        
        beforeEach(function() {
            baseURI = "http://www.test.com/pages/"
            wikiPage = "NewPage";
            currPage = baseURI + wikiPage;
            windowMock = { 'location': { 'href': currPage } };
        });
        
        it('should redirect if response successfully updates page and curr page URL contains terminating slash', function() {
            var xmlHttpRequestMock = { 'readyState': 4, 'status': 200, 'responseText': '{}'};
            windowMock.location.href = windowMock.location.href+ "/"
            
            handleDeletePageResponse(xmlHttpRequestMock, windowMock);
            
            expect(windowMock.location).toEqual(baseURI + "new/");
        });
        
        it('should redirect if response successfully updates page and curr page URL does not contain terminating slash', function() {
            var xmlHttpRequestMock = { 'readyState': 4, 'status': 200, 'responseText': '{}'};
            
            handleDeletePageResponse(xmlHttpRequestMock, windowMock);
            
            expect(windowMock.location).toEqual(baseURI + "new/");
        });
        
        it('should not redirect if response contains errors', function() {
            var xmlHttpRequestMock = { 'readyState': 4, 'status': 200, 'responseText': '{"errors": ["test1", "test2"]}' };
            
            handleDeletePageResponse(xmlHttpRequestMock, windowMock);
            
            expect(windowMock.location.href).toEqual(currPage);
        });
        
        it('should not redirect if the response status is not 200', function() {
            var xmlHttpRequestMock = { 'readyState': 4, 'status': 404, 'responseText': '{}'};
            
            handleDeletePageResponse(xmlHttpRequestMock, windowMock);
            
            expect(windowMock.location.href).toEqual(currPage);
        });
        
        it('should not redirect if the readyState is not 4', function() {
            var xmlHttpRequestMock = { 'readyState': 3, 'status': 200, 'responseText': ''};
            
            handleDeletePageResponse(xmlHttpRequestMock, windowMock);
            
            expect(windowMock.location.href).toEqual(currPage);
        });
    });
});