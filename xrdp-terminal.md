# Xrdp terminal이 다른 곳에 뜰 때

* default terminal을 바꿔줘야함

```bash
sudo update-alternatives --config x-terminal-emulator
```

기본은 `/usr/bin/gnome-terminal.wrapper` 터미널이였지만 `/usr/bin/xfce4-terminal.wrapper` 로 바꿔주고 난 후에 정상 동작함.

xrdp 에서 xfce4는 제대로 동작했지만 xfce4 terminal도 설치해주고 default terminal을 그것으로 바꿔줘야만 했다.



