*** Settings ***
Library        MyLibrary.py

Suite Setup    Call Suite Setup Function

*** Test Cases ***
My Test Case1
    Log    Running Test Case

*** Keywords ***
Call Suite Setup Function
    MyLibrary.helloworld
    MyLibrary.reset           ${123}