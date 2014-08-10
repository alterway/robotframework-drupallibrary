*** Settings ***
Documentation     Remove members added by the addmembers.robot suite
Resource          resources.robot
Library           Selenium2Library
Library           DrupalLibrary    ${HOME URL}

*** Test Cases ***
Open Home Page
    Open Browser    ${HOME URL}    ${BROWSER}
    Maximize Browser Window

Signing In
    Sign In    ${WM NAME}    ${WM PASS}    stop_on_failure=${false}

Removing Some Members
    Comment    Remove completely member johndoe
    Remove Member    johndoe    policy=user_cancel_delete
    Comment    Blockin member janedoe with default behaviour
    Remove Member    janedoe
    Comment    Blockin member foobar and reassign its content
    Remove Member    foobar    policy=user_cancel_reassign

Attempt to remove a unknown user
    Comment    We know this will fail
    Remove Member    nosuchanuser    exit_on_failure=${false}
