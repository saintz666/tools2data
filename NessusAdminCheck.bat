## Script to check if remote scan is enabled.

@echo off

echo "Checking Remote Registry"

for /F "tokens=3 delims=: " %%H in ('sc query "remoteregistry" ^| findstr "STATE"') do (
  if /I "%%H" NEQ "RUNNING" (
  	  sc config remoteregistry start=demand
      net start "remoteregistry"
  )
)

reg query \\127.0.0.1\hklm

echo "Checking SMB service"

for /F "tokens=3 delims=: " %%H in ('net use \\127.0.0.1\ipc$ "" /user:"" ^| findstr "STATE"') do (
  if /I "%%H" NEQ "RUNNING" (
  	  sc config remoteregistry start=demand
      net start "remoteregistry"
  )
)
net use \\127.0.0.1\ipc$ "" /user:""
net use \\127.0.0.1\admin$ "" /user:""
