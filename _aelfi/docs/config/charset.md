## Charset

Right now, the only runtime configuration you have control over is `Charset`, but we may add more, like BYO templating engines and stuff. The charset is obvious to set, it a single directive, you can choose what ever you want:
```YAML
Charset: 'utf-8'	# utf-8 is best!
```
You **must not *ever* remove** the Charset directive; if you don't think you need it, then leave it alone.

We advise you sticking to `utf-8`, for the sake of everyone, including yourself. However, if you want to use another charset, any one which is both supported by the web and, more importantly to get it to run, Python *(old list available [here](https://docs.python.org/2.4/lib/standard-encodings.html))*, should work just fine!