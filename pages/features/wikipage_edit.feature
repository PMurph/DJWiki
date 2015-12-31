Feature: As a software developer,
    I want to be able to update wiki pages,
    so that I can added information on new features I'm adding to my projects.
    
Scenario: Viewing the edit page
    Given that the TestProject page exists
    And given that I view the TestProject page
    It should have a link to the edit operation page
    Given that I view the TestProject edit operation page
    It should have a place to enter the title of the page
    And it should have a place to enter the page_content of the page
    
 Scenario: Editing a wiki page
    Given that the EditTestPage page exists
    And given that I view the EditTestPage edit operation page
    And given that I enter "EdittedTestPage" as the title
    And given that I enter "This is a test to see if the editting feature is working" as the page_content
    And given that I save the edits
    I should receive a message stating that the EditTestPage page has been saved
    Given that I view the EditTestPage detail operation page
    It should have "EdittedTestPage" as the title
    And it should have "EdittedTestPage" as the h1 heading
    And it should have "This is a test to see if the editting feature is working" as the content