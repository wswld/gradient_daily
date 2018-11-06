# Daily Gradient Bot for Instagram

This bot does just that: it generates a gradient image and pushes it to Instagram ([@gradientdaily](https://www.instagram.com/gradientdaily/)).

![Look, ma, it's a gradient!](/example.jpg)

*This image is resized, originally they are 1080x1080.*

## Installation

Since we're going to be using Pillow and other hardcore stuff, here's a list of dependencies:

``` bash
sudo apt-get install libcurl4-openssl-dev python-dev libssl-dev libtiff5-dev
sudo apt-get install zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
```
Then I usually do the following:

``` bash
git clone https://github.com/wswld/gradient_daily.git $PROJDIR
cd $PROJDIR
virtualenv .env
.env/bin/pip install -r requirements.txt
```
Of course you may have a better idea or try some kinky stuff. I don't judge.

Then you should be able to run:

``` sh 
.env/bin/gradient-daily --login XXXX --passwd YYYY --writepath /tmp 
```

That's it.

PS: This code is not really RAM-efficient, so if you're running it on a 500Mb machine, time to create some swap.