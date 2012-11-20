@echo off
if exist CodeGenerater.class (goto run) else (goto compile)
:nothing
goto end
:compile
javac CodeGenerater.java
goto run
:run
java -cp . CodeGenerater
:end
pause