Feature: As a sales associate,
    I want to be able to view wiki pages,
    so that I can get information on the projects I am selling to the customer.
    
Scenario: Viewing created page
    Given that the TestProject page exists
    And given that I view the TestProject page
    It should have "TestProject" as the title
    And it should have "TestProject" as the h1 heading
    And it should have "This is a test project" as the content
