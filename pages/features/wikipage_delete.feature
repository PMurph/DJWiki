Feature: As a software maintainer,
    I want to delete pages,
    so that I can stop supporting deprecated software.
    
Scenario: Viewing the delete button
    Given that the DeleteTestProject page exists
    And given that I view the DeleteTestProject page
    It should have a "Delete" button

Scenario: Deleting a page
    Given that the DeleteTestProject page exists
    And givne that I delete the DeleteTestProject page
    The DeleteTestProject page should no longer exist