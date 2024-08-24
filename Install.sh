!#/bin/bash
sudo pacman -S git pyside6
git clone https://Carl:%40Ankor15@cordlessblues.com/git/repos/carl/pluto.git ~/Documents/Pluto
mkdir -p ~/.config/Pluto/
mv ~/Documents/Pluto/Config.Json ~/.config/Config.Json
mv ~/Documents/Pluto/Pluto.png ~/.config/Pluto.png
mv ~/Documents/Pluto/Pluto.py /opt/Pluto/
cp ~/Documents/Pluto/com.cordlessblues.Pluto.desktop ~/.local/share/applications/com.cordlessblues.Pluto.desktop
echo "install complete"
clear
python3 ~/Documents/Pluto/Pluto.py
