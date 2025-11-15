
IAF Quiz GitHub Repo
====================

Contents:
- main.py            : PyQt5 touchscreen-style quiz app
- questions.json     : 200-question IAF quiz bank (editable)
- .github/workflows  : GitHub Actions workflow to build Windows .exe (IAF_Quiz.exe)

How to use:
1. Create a new GitHub repository (public or private).
2. Upload the contents of this zip to the repository root.
3. Commit and push to `main` branch.
4. Go to the Actions tab -> Build Windows EXE -> Run workflow (or push to main to trigger).
5. Wait for the workflow to complete; download the artifact named `IAF_Quiz_windows_exe` which contains `IAF_Quiz.exe`.

Notes:
- The exe is built on a Windows runner using PyInstaller and includes the questions.json bundled.
- If GUI fails on target machine, install Microsoft Visual C++ Redistributable (latest).
- You can edit questions.json in the repo and re-run the workflow to produce a new exe.
