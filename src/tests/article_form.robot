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
    Successfully Created Article

Adding a duplicate article results in error message
    Go To  ${NEW_ARTICLE_URL}
    Input Text  author  Matti
    Input Text  title  Tutkimusartikkeli
    Input Text  journal  Scientific American
    Input Text  year  1989
    Click Button  Create
    Successfully Created Article
    Go To  ${NEW_ARTICLE_URL}
    Input Text  author  Matti
    Input Text  title  Tutkimusartikkeli
    Input Text  journal  Scientific American
    Input Text  year  1989
    Click Button  Create
    Failed To Create Article
    
The article reference can be viewed after adding
    Go To  ${NEW_ARTICLE_URL}
    Input Text  author  Teppo
    Input Text  title  Tepon kirjoitelma
    Input Text  journal  Scientific American
    Input Text  year  2000
    Click Button  Create
    Successfully Created Article
    Go To  ${REFS_URL}
    Page Should Contain  Tepon kirjoitelma

The article bibtex can be copied to clipboard
    [Tags]  clipboard
    Go To  ${NEW_ARTICLE_URL}
    Input Text  author  Teppo
    Input Text  title  Tepon kirjoitelma
    Input Text  journal  Scientific American
    Input Text  year  2000
    Click Button  Create
    Successfully Created Article
    Go To  ${REFS_URL}
    Click Link  article
    Click Button  Copy BibTeX
    Page Should Contain  Copied!

