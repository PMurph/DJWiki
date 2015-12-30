Feature: As a software developer,
    I want to be able to update wiki pages,
    so that I can added information on new features I'm adding to my projects.
    
Scenario: Viewing the edit page
    Given that the TestProject page exists
    And given that I view the TestProject page
    It should have a link to the link to the edit page
    Given that I view the TestProject edit page
    It should have a place to enter the title of the page
    And it should have a place to enter the page_content of the page