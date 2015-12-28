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
    And given that I enter "NewProject" as the title 
    And given that I enter "This is for a test" as the page_content
    And given that I create the page
    I should receive a message stating the NewProject page was created
    Given that I view the NewProject page
    I should see the "NewProject" page

Scenario: Creating page that already exists
    Given that the ThirdProject page exists
    And given that I view the new page form
    And given that I enter "ThirdProject" as the title
    And given that I enter "This is a test to ensure that I cannot create duplicate pages" as the page_content
    And given that I create the page
    I should receive a message stating there was an error creating the page