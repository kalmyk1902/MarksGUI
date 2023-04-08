@echo off

if not exist ..\localization\ (
    mkdir ..\localization\
)

curl -o .\localization\locale.xml https://raw.githubusercontent.com/kalmyk1902/MarksGUI/main/localization/locale.xml -OL