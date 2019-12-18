# Musicript

Musicript is a fully hackable framework that enables you to write any music with Python and Python only!
This is also a revival of musicript that was [originally written in .NET & XML](https://github.com/Mygod/musicript/tree/csharp).

Why Musicript:

* No more copy-pasting your musical idea (repetition is fundamental to music but modern music softwares do not quite respect that);
* Everything fully hackable, including:
    - All temperaments are equal; (check out `temperaments.py`)
    - You get to describe every single detail of your desired tone color, or you can just import other instruments;
* Version control friendly;
* Similar to [ChucK](http://chuck.stanford.edu/), except that you do not need to learn some obscure new language to use it!
* Python and therefore Turing complete.

## Getting started

```bash
pipenv install -d
python towav.py tests.simple <output.wav>
python tospeaker.py tests.simple
```

Also check out other music in `tests`!

## How does it work?

`Track` takes a generator object (which is outputted by a function that `yield`s, this is how we enable infinite loops), and manipulate its global environment to add new methods that you can call.
These methods will in turn enable the inner function to manipulate the environment.
The function sets up the environment before it yields and suspends itself.
In between the suspension, Musicript reads out the environment and generates audio samples.

`track_worker` recompiles your method into the one that yields every timeout that is outputted by its subroutines that are also tagged `track_worker` (and copies its global environment into subroutine's global environment).
It also sets up an isolated global environment every time the function is run, so that `Track` can manipulate each generator object without affecting the rest of the world. 

## Known issues

* I have not tested `tospeaker.py` because of Linux;
* Python IDEs do not quite like music written in Python, yet! (an IDE plugin might fix this)
