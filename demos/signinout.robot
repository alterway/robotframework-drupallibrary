*** Settings ***
Documentation     A small sign-in sign-out demo that logs in and out the
...               Drupal demo site.
Resource          resources.robot
Library           Selenium2Library
Library           DrupalLibrary    ${HOME URL}

*** Test Cases ***
Open Home Page
    Open Browser    ${HOME URL}    ${BROWSER}
    Maximize Browser Window

Signing In
    Sign In    ${WM NAME}    ${WM PASS}    exit_on_failure=${false}

Signing Out
    Logout

Back Home
    Go To Home Page
