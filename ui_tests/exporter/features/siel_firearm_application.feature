Feature: I want to be able to submit SIEL firearm applications
  As a logged in exporter
  I want to be able to submit SIEL firearm applications

  Scenario: Initiate an application for a SIEL firearm
    Given I signin and go to exporter homepage and choose Test Org
    When I create a standard application of a "temporary" export type
    Then I see the application overview
    And I logout

  Scenario: Open a SIEL application
    Given I signin and go to exporter homepage and choose Test Org
    When I click on applications
    And I click on draft tab for applications
    And I click on the application just created
    Then I see the application overview
    And I logout

  Scenario: Temporary export details
    Given I signin and go to exporter homepage and choose Test Org
    When I click on applications
    And I click on draft tab for applications
    And I click on the application just created
    And I click on "Temporary export details"
    And I provide details of why my export is temporary
    And I answer "Yes" for whether the products remain under my direct control
    And I enter the date "01", "01", "2030" when the products will return to the UK
    Then I see the temporary export detail summary
    And I logout

  Scenario: Add a new Firearm product of type firearms, ammunition, components of ammunition to the application
    Given I signin and go to exporter homepage and choose Test Org
    When I create a standard application of a "permanent" export type
    When I click on the "Products" section
    And I choose to add a new product
    And I select product category "firearms"
    And I select product type "firearm"
    And I select sporting shotgun status as "Yes"
    And I specify number of items as "4"
    And I select "Yes" for serial number or other identification markings with details as " "
    And I enter "4" serial numbers as "serial1,serial2,serial3,serial4"
    And I enter good name as "Rifle" description as "new firearm" part number "FR-123-M" controlled "True" control code "PL9002" and graded "no"
    And I enter firearm year of manufacture as "2020"
    And I select firearm replica status as "Yes" with description "More details about the replica"
    And I enter calibre as "0.22"
    And I select "No" to registered firearms dealer question
    And I specify firearms act sections apply as "Yes"
    And I select firearms act section "2"
    And I upload firearms certificate file "file_for_doc_upload_test_1.txt"
    And I enter certificate number as "FR2468/1234/1" with expiry date "12-10-2030"
    And I see summary screen for "Firearms" product with name "Rifle" and "continue"
    And I select "Yes" to document available question
    And I select "No" to document is above official sensitive question
    And I upload file "file_for_doc_upload_test_1.txt" with description "File uploaded for firearms product."
    And I enter product details with value "20,000" and deactivated "No" and Save
    Then the product with name "Rifle" is added to the application
    And I logout


  Scenario: Enter details for the End use details section in the application
    Given I signin and go to exporter homepage and choose Test Org
    When I create a standard application of a "permanent" export type
    And I am on the application overview page entitled "Standard Individual Export Licence"
    When I click on the "End use details" section
    And I provide details of the intended end use of the products
    And I answer "No" for informed by ECJU to apply
    And I answer "No" for informed by ECJU about WMD use
    And I answer "No" for suspected WMD use
    And I answer "No" for products received under transfer licence from the EU
    And I save and continue on the summary page
    Then I should be taken to the application overview page entitled "Standard Individual Export Licence"
    And the section "End use details" is now saved
    And I logout


  Scenario: Enter details for the Route of goods section in the application
    Given I signin and go to exporter homepage and choose Test Org
    When I create a standard application of a "permanent" export type
    And I am on the application overview page entitled "Standard Individual Export Licence"
    When I click on the "Route of goods" section
    And I answer "Yes" for shipping air waybill or lading and Save
    Then I should be taken to the application overview page entitled "Standard Individual Export Licence"
    And the section "Route of goods" is now saved
    And I logout


  Scenario: Enter details for the Location section in the application
    Given I signin and go to exporter homepage and choose Test Org
    When I create a standard application of a "permanent" export type
    And I am on the application overview page entitled "Standard Individual Export Licence"
    When I click on the "Locations" section
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I click the back link
    Then I should be taken to the application overview page entitled "Standard Individual Export Licence"
    And the section "Locations" is now saved
    And I logout
