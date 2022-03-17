@all @internal @view_cases
Feature: I want to view the case details of a case
  As a Logged in government user
  I want to view the details on a case
  So that I can make review the case before making any decisions

  Scenario: Gov user can see case details
    Given I sign in to SSO or am signed into SSO
    And I create an application with <name>,<product>,<part_number>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    And the status is set to "submitted"
    When I go to the case list page
    And I click on show filters
    And I filter by application type "Standard Individual Export Licence"
    Then I should see my case in the cases list
    When I go to application previously created
    Then I should see the product name as "Rifle" with product rating as "PL9002"
    And the "Consignee" name is "Automated Consignee", address is "1234, Trade centre", country is "Belgium"
    And the "End user" name is "Automated End user", address is "1234, High street", country is "Belgium"
    And the intended end use details should be "Research and development"

    Examples:
    | name    | product | part_number | clc_rating  | end_user_name      | end_user_address  | country | consignee_name      | consignee_address   | end_use                  |
    | Test    | Rifle   | PN-123/XYZ  | PL9002      | Automated End user | 1234, High street | BE      | Automated Consignee | 1234, Trade centre  | Research and development |


  Scenario: Gov user can view product document
    Given I sign in to SSO or am signed into SSO
    And I create an application with <name>,<product>,<part_number>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    And the status is set to "submitted"
    When I go to the case list page
    And I click on show filters
    And I filter by application type "Standard Individual Export Licence"
    Then I should see my case in the cases list
    When I go to application previously created
    And I click on "Documents" tab
    Then I should see a link to download the document

    Examples:
    | name    | product | part_number  | clc_rating  | end_user_name      | end_user_address  | country | consignee_name      | consignee_address   | end_use                  |
    | Test    | Rifle   | SN-PN-123/AB | PL9002      | Automated End user | 1234, High street | BE      | Automated Consignee | 1234, Trade centre  | Research and development |


  @skip @legacy
  Scenario: Gov user can see all parties on the case
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    # Ensure the application is in a submitted state in case workflow has been run
    And the status is set to "submitted"
    When I go to the case list page
    Then I should see my case in the cases list
    And I should see my case SLA
    When I go to application previously created
    Then I see the application destinations
    And I should see the view link displayed against a good
    Given the exporter has deleted the third party
    When I go to application previously created
    Then I see an inactive party on page
    When I go to the documents tab
    Then I see my autogenerated application form

  @skip @legacy
  Scenario: Gov user can see exporter has made changes to case
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    # Ensure the application is in a submitted state in case workflow has been run
    And the status is set to "submitted"
    And I am an assigned user for the case
    And the exporter user has edited the case
    When I go to the internal homepage
    And I click on the exporter amendments banner
    Then I can see the case on the exporter amendments queue
    When I go to application previously created
    Then I see that changes have been made to the case
    When I go to the documents tab
    Then I see my autogenerated application form
