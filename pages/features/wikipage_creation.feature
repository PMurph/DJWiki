Feature: As a project manager,
    I want to be able to create new wiki pages,
    so that I can store the requirements of my team's project.
    
Scenario: Viewing the new page form
    Given that I view the new page form
    The page should have a place to enter the title of the page
    And the page should have a place to enter the content of the page

Scenario: Creating a new page
    Given that the NewProject page does not exist
    And given that I view the new page form
    And given that I enter NewProject as the title and "This is for a test" as the content
    I should see the newly created "NewProject" page
    