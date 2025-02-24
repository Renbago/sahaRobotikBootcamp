; Ctrl + Shift + C ile kopyalama (Ctrl + C simüle edilir)
^+c::Send "^c"

; Ctrl + Shift + V ile yapıştırma (Ctrl + V simüle edilir)
^+v::Send "^v"

; WSL başlat
^!t::Run "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -NoExit -Command wsl -e bash -c 'clear; cd ~; bash'"
