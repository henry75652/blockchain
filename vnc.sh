sudo apt update
sudo apt-get install python3-pip 
python3 -m pip install pycryptodome
python3 - pip install cryto
python3 - pip install ecdsa
sudo apt install vino
sudo apt autoremove
mkdir -p ~/.config/autostart
cp /usr/share/applications/vino-server.desktop ~/.config/autostart
gsettings set org.gnome.Vino prompt-enabled false
gsettings set org.gnome.Vino require-encryption false
gsettings set org.gnome.Vino authentication-methods "['vnc']"
gsettings set org.gnome.Vino vnc-password $(echo -n 'jetson'|base64)
