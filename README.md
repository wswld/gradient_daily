# Daily Gradient Bot for Instagram

This bot does just that: it generates a gradient image and pushes it to Instagram ([@gradientdaily](https://www.instagram.com/gradientdaily/)).

![Look, ma, it's a gradient!](/example.jpg)

*This image is resized, originally they are 1080x1080.*

## Installation

Since we're going to be using Pillow and other hardcore stuff, here's a list of dependencies:

``` bash
sudo apt-get install libcurl4-openssl-dev python-dev libssl-dev libtiff5-dev libjpeg62-turbo-dev
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

## Common Problems

- You may get a weird error about a `.dat` file. You may need to run:

    ``` sh 
    mkdir -p .env/lib/python2.7/site-packages/src/data/
    ```

    This is a dirty hack, I'm not sure why it's not created in the first place, but:

    ![Ain't nobody got time for that!](http://i.giphy.com/bWM2eWYfN3r20.gif)

- This code is not really RAM-efficient, so if you're running it on a 500Mb machine, time to create some swap.