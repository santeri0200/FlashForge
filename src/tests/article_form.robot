*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Articles



*** Test Cases ***
Adding a new article with the form
    Go To  ${NEW_ARTICLE_URL}
    Input Text  author  Matti
    Input Text  title  Tutkimusartikkeli
    Input Text  journal  Scientific American
    Input Text  year  1989
    Click Button  Create
    Page Should Contain  Welcome page

Adding a duplicate article results in error message
    Go To  ${NEW_ARTICLE_URL}
    Input Text  author  Matti
    Input Text  title  Tutkimusartikkeli
    Input Text  journal  Scientific American
    Input Text  year  1989
    Click Button  Create
    Go To  ${NEW_ARTICLE_URL}
    Input Text  author  Matti
    Input Text  title  Tutkimusartikkeli
    Input Text  journal  Scientific American
    Input Text  year  1989
    Click Button  Create
    Page Should Contain  Virheelliset tiedot
    
The article reference can be viewed after adding
    Go To  ${NEW_ARTICLE_URL}
    Input Text  author  Teppo
    Input Text  title  Tepon kirjoitelma
    Input Text  journal  Scientific American
    Input Text  year  2000
    Click Button  Create
    Go To  ${REFS_URL}
    Page Should Contain  Tepon kirjoitelma