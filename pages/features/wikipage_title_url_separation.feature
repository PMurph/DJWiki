Feature: As a student,
    I want to be able to have two different pages with the same title,
    so that I can have a page for something that has different meaning in different contexts.
    
Scenario: Viewing two pages that have the same title
    Given that the SomeTopic-Math page exists
    And given that I view the SomeTopic-Math page
    It should have "SomeTopic" as the title
    And it should have "SomeTopic" as the h1 heading
    Given that the SomeTopic-Science page exists
    And given that I view the SomeTopic-Science page
    It should have "SomeTopic" as the title
    And it should have "SomeTopic" as the h1 heading
