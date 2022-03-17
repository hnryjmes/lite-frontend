@all @open
Feature: View an Open Applications

  @skip @legacy
  Scenario: View an Open Application
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    When I go to the case list page
    Then I should see my case in the cases list
    And I should see my case SLA
    When I go to application previously created
    Then I see the case page
    When I go to the activity tab
    When filter user_type has been changed to "Exporter"
    Then exporter is at the first audit in the trail
    When filter user_type has been changed to "Internal"
    Then exporter is not in the audit trail
    When I go to the documents tab
    Then I see my autogenerated application form


  @skip @legacy
  Scenario: View an Open Application and set a next review date
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    And a queue has been created
    And case has been moved to new Queue
    When I go to my work queue
    Then I should see my case in the cases list
    When I go to application previously created
    Then I see the case page
    When I click set next review date button
    And I enter a next review date
    Then I see the review date has been set
    When I go to the activity tab
    Then review date is at the first audit in the trail
    # The case should be hidden as the next review date is in the future
    When I go to my work queue
    Then I don't see previously created application
    # After applying hidden cases filter then the case should no longer be hidden
    Then I see previously hidden created application
    # The case should not be hidden in all cases queue
    When I go to the case list page
    Then I see previously created application
