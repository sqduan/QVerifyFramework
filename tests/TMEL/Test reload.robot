*** Variables ***
${RUMI_NAME}
${SETTINGS}
${PLATFORM_CONFIG}

*** Settings ***
Documentation      A test suite for verify RUMI operations
Resource           ../../resources/common.resource
Suite Setup        Reload Image     blr-s4b-q07558     9999    600

*** Test Cases ***
Wait Until Load Finish
    ${result}=     Sleep     300
    Should be equal    ${result}    ${0}

Do Rumi Reset
    ${result}=     Reset Rumi     blr-s4b-q07558     9999    600
    Should be equal    ${result}    ${0}

Do Jtag Reset
    ${result}=     Reset Jtag     blr-s4b-q07558     9999    600
    Should be equal    ${result}    ${0}

Do Rumi Quit
    ${result}=     Quit Rumi     blr-s4b-q07558     9999    600
    Should be equal    ${result}    ${0}
