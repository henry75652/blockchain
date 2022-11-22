sudo apt update
pip install pycryptodome
pip install cryto
sudo pip install ecdsa
echo 'export PATH=/home/ideiowo/.local/bin:$PATH' >>~/.bashrc~
source ~/.bashrc
export PATH=$PATH:/home/ideiowo/.local/bin
source $HOME/.bashrc
sudo apt install vino
mkdir -p ~/.config/autostart
cp /usr/share/applications/vino-server.desktop ~/.config/autostart
gsettings set org.gnome.Vino prompt-enabled false
gsettings set org.gnome.Vino require-encryption false
gsettings set org.gnome.Vino authentication-methods "['vnc']"
gsettings set org.gnome.Vino vnc-password $(echo -n jetson'|base64)
sudo reboot
