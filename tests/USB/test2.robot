*** Settings ***
Library        MyLibrary.py

Suite Setup    Call Suite Setup Function

*** Test Cases ***
My Test Case2
    Log    Running Test Case

*** Keywords ***
Call Suite Setup Function
    MyLibrary.helloworld