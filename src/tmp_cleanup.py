import os
import subprocess
import sys

def cleanup():
    try:
        # Get all python processes
        output = subprocess.check_output(['Get-WmiObject', 'Win32_Process', '-Filter', "name='python.exe'"], shell=True, text=True)
        # This is a bit complex in pure python via subprocess shell, let's use powershell directly
        ps_script = """
        Get-WmiObject Win32_Process -Filter "name='python.exe'" | ForEach-Object {
            if ($_.CommandLine -like "*autonomy_loop.py*") {
                Write-Host "Killing Process: $($_.ProcessId) - $($_.CommandLine)"
                Stop-Process -Id $_.ProcessId -Force
            }
        }
        """
        subprocess.run(['powershell', '-Command', ps_script], check=True)
        print("Cleanup completed.")
    except Exception as e:
        print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    cleanup()
