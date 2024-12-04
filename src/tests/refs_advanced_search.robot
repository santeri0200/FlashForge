*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Setup Search

*** Test Cases ***
Advanced search by author
    Select From List By Label  field  author
    Input Text  advanced_query  ma
    Click Button  Search
    Page Should Contain  Found 1 reference:
    Page Should Contain  Tutkimusartikkeli

Advanced search by title
    Select From List By Label  field  title
    Input Text  advanced_query  kimusart
    Click Button  Search
    Page Should Contain  Found 1 reference:
    Page Should Contain  Tutkimusartikkeli

Advanced search by journal
    Select From List By Label  field  journal
    Input Text  advanced_query  merican
    Click Button  Search
    Page Should Contain  Found 1 reference:
    Page Should Contain  Tutkimusartikkeli

Advanced search by year
    Select From List By Label  field  year
    Input Text  advanced_query  1989
    Click Button  Search
    Page Should Contain  Found 1 reference:
    Page Should Contain  Tutkimusartikkeli

Advanced search non existing
    Select From List By Label  field  all fields
    Input Text  advanced_query  8000
    Click Button  Search
    Page Should Contain  No results.

*** Keywords ***
Setup Search
    Reset Articles
    Go To  ${HOME_URL}
    Main Page Should Be Open
    Click Link  Create article reference
    Input Text  author  Matti
    Input Text  title  Tutkimusartikkeli
    Input Text  journal  Scientific American
    Input Text  year  1989
    Click Button  Create
    Main Page Should Be Open
    Click Link  Advanced search