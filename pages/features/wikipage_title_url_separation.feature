Feature: As a student,
    I want to be able to have two different pages with the same title,
    so that I can have a page for something that has different meaning in different contexts.
    
Scenario: Creating a page with different url and titles
    Given that the DifferentTitleAndUrlProject page does not exist
    And given that I view the new page form
    And given that I enter "DifferentTitleAndUrlProject" as the title
    And given that I enter "diff-url" as the page_url
    And given that I enter "This is for a test" as the page_content
    And given that I create the page
    And given that I view the diff-url page
    I should see the "DifferentTitleAndUrlProject" page
    
Scenario: Viewing two pages that have the same title
    Given that the SomeTopic-Math page exists
    And given that I view the SomeTopic-Math page
    It should have "SomeTopic" as the title
    And it should have "SomeTopic" as the h1 heading
    Given that the SomeTopic-Science page exists
    And given that I view the SomeTopic-Science page
    It should have "SomeTopic" as the title
    And it should have "SomeTopic" as the h1 heading
