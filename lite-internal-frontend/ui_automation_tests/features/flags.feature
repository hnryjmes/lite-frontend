Feature:  I want to create and deactivate case flags
  As a logged in government user
  I want to create and deactivate case flags
  So that I can make new flags where required and prevent flags which are no longer relevant from being assigned to cases

  Scenario: Create new flag
    Given I go to internal homepage
    When I go to flags
    And I add a flag called "flag-t" at level "Case"
    Then I see the flag in the flag list
    When I add an existing flag name
    Then I see error message "Enter a name which is not already in use by another flag"

  Scenario: Add a flag with empty field
    Given I go to internal homepage
    When I go to flags
    And I add a flag called " " at level "Case"
    Then I see error message "Flag name may not be blank"

  Scenario: Add a flag with over 20 characters field
    Given I go to internal homepage
    When I go to flags
    And I add a flag called "aaaaaaaaaaaaaaaaaaaaa" at level "Case"
    Then I see error message "Ensure this field has no more than 20 characters."

  Scenario: Edit a flag
    Given I go to internal homepage
    When I go to flags
    And I add a flag called "Flag-e" at level "Case"
    And I edit my flag
    Then I see the flag in the flag list

  Scenario: Deactivate and reactivate a flag
    Given I go to internal homepage
    When I go to flags
    And I count the number of active flags
    And I deactivate the first active flag
    And I click include deactivated
    Then I see one less active flags
    When I reactivate the first deactivated flag
    Then I see the original number of active flags
