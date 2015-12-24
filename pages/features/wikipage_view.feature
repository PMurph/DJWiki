Feature: As a sales associate,
    I want to be able to view wiki pages,
    so that I can get information on the projects I am selling to the customer.
    
Scenario: Viewing created page
    Given that the TestProject page exists
    And given that I view the TestProject page
    The page should have the title TestProject
    And the page's main heading should be "TestProject"
    And it should contain the text "This is a test project"
