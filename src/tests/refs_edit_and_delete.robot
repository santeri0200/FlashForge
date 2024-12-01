*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Setup References

*** Test Cases ***
Editing references successfully
    Click Link  Edit reference
    Input Text  year  1987
    Click Button  Save changes
    Page Should Contain  1987
    Title Should Be  Article reference

Deleting references successfully
    Click Link  Delete reference
    Click Button  Delete
    Main Page Should Be Open

*** Keywords ***
Setup References
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
    Click Link  References list
    Click Link  View reference