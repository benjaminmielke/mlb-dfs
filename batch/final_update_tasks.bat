
C:\Windows\System32\schtasks.exe /create /tn YS-run_final_update0 /sc daily /st 12:10 /tr C:\Users\okiem\github\mlb-dfs\batch\run_final_update.bat /f
C:\Windows\System32\schtasks.exe /create /tn YS-run_final_update1 /sc daily /st 18:15 /tr C:\Users\okiem\github\mlb-dfs\batch\run_final_update.bat /f
C:\Windows\System32\schtasks.exe /create /tn YS-run_final_update2 /sc daily /st 21:10 /tr C:\Users\okiem\github\mlb-dfs\batch\run_final_update.bat /f
C:\Windows\System32\schtasks.exe /create /tn YS-run_final_update3 /sc daily /st 15:07 /tr C:\Users\okiem\github\mlb-dfs\batch\run_final_update.bat /f