import subprocess

if __name__ == '__main__':
    picture_path = '/mnt/82B69084B69079FD/python_project/parser-ya-images/3.jpg'
    subprocess.Popen("DISPLAY=:0 GSETTINGS_BACKEND=dconf /usr/bin/gsettings set org.gnome.desktop.background picture-uri file://{0}".format(picture_path), shell=True)

cmd = "source ./mnt/82B69084B69079FD/python_env/parser-ya-images/bin/activate"
process = subprocess.Popen(cmd, stdout=PIPE, shell=True)
python python /mnt/82B69084B69079FD/python_project/parser-ya-images/main.py
alias venv="source /mnt/82B69084B69079FD/python_env/parser-ya-images/bin/activate"
venv
#!/bin/bash
activate(){
    . ./mnt/82B69084B69079FD/python_env/parser-ya-images/bin/activate
}
activate