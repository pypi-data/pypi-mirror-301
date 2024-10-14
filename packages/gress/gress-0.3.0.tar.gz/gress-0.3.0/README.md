#  Gress - Naïve Progress Bar

What should be the amateur version of *progress* - a ***gress***? The *gress* library provide highly customizable
text-based progress monitor for *Python*. The inspiration for this library came from the original work of
[Nilton Volpato](https://github.com/NiltonVolpato/python-progressbar), but it was recreated from scratch to make it
easier to set up and use.

### Example 1

```python
import time
from gress import gress

# counting sheep
for i in gress(range(100)):
    time.sleep(0.1)


# output during processing
# 81 of 100 (81%) █████████████████████████████-------- 00:00:08 | 9.54/s | ETA 1s
```

### Example 2

```python
import time
from gress import gress

# init herd
sheep = (i for i in range(100))

# counting sheep
for i in gress(sheep, maximum=100):
    time.sleep(0.1)


# output during processing
# 46 of 100 (46%) █████████████████-------------------- 00:00:04 | 9.66/s | ETA 5s
```

### Example 3

```python
import time
from gress import gress

# counting sheep
for i in gress(range(100), "{percent} % {bar} ETA {autoeta}", size=40):
    time.sleep(0.1)


# output during processing
# 46 % ████████████---------------- ETA 5s
```

### Example 4

```python
import time
import gress

# init herd
sheep = 100

# init bar
bar = gress.Bar("Counting: {count} of {maximum} ({percent}%) {bar} {speed}/s | {timer} | ETA {autoeta}", maximum=sheep)

# counting sheep
for i in bar(range(sheep)):
    time.sleep(0.1)

# write final report
bar.write("All {count} sheep counted in {autotimer} with the average rate of {speed}/s.")


# output during processing
# Counting: 56 of 100 (56%) ███████████████------------ 9.63/s | 00:00:05 | ETA 4s

# output after processing
# All 100 sheep counted in 10s with the average rate of 9.65/s.
```

### Example 5

```python
import time
import gress

# init herd
sheep = 100

# init bar
bar = gress.Bar("Counting: {count} of {maximum} ({percent}%) {bar} {speed}/s | {timer} | ETA {autoeta}", maximum=sheep)
bar.start()

# counting sheep
sleep = 0.1
for i in range(sheep):
    time.sleep(sleep)
    
    # increment progress
    bar += 1
    
    # count slower while sleeping (50 sheep and more)
    if bar.current == sheep / 2:
        bar.write("{time} I should sleep now, so I'm counting slower!")
        sleep *= 2

# finish and make final report
bar.finish("{time} All {count} sheep counted in {autotimer} with the average rate of {speed}/s.")


# output during processing
# 2022-10-01 21:12:13.565873 I should sleep now, so I'm counting slower!
# Counting: 77 of 100 (77%) ████████████████████------ 4.95/s | 00:00:10 | ETA 4s

# output after processing
# 2022-10-01 21:12:13.565873 I should sleep now, so I'm counting slower!
# 2022-10-01 21:12:23.478325 All 100 sheep counted in 15s with the average rate of 6.47/s.
```


## Progress Bar

The best way to monitor progress is to initialize the **Bar** object with a custom template, using predefined
widgets and continuously increase its value (see the example above). Although this should cover most of the use cases,
there are many ways to go deeper to customize the main progress bar or individual widgets.

    widgets: (Widget,) or str
        Collection of widgets to display on each update. The widget can be one of
        the many predefined widgets, simple string to show or any class derived from
        the Widget base. The widgets can also be provided using a template, where
        the widgets are specified by a name in curly brackets
        (e.g. 'Processed: {count} ETA: {eta}').
    
    minimum: int
        Minimum progress value or count.
    
    maximum: int
        Maximum progress value or count.
    
    size: int
        Number of characters available to display the progress.
    
    refresh: float
        Minimum number of seconds between individual updates to be displayed.
    
    sample: int
        Number of last sample to keep for adaptive widgets like ETA
        or speed. Such widgets are calculating progress from last
        measurements instead of overall progress.
    
    output: any
        Custom output to which all the progress and messages are writen. This must support
        'write' and 'flush' method calls.


### Widgets initialization

**By template** - This is probably the most convenient method of widgets initialization. It is based on
recognizing predefined or registered widgets by their unique tags within a single template string. The widgets are
specified using the **{tag}** syntax.

```python
bar = gress.Bar("Counting: {count} of {maximum} sheep. Ready in {autoeta}.", maximum=100)
```

**By widgets** - If none of the predefined widgets suits your needs, custom instances can be provided directly.

```python
bar = gress.Bar(
    "Counting: ",
    gress.Property("current", "{:03}"), " of ", gress.Property("maximum"),
    " sheep. Ready in ",
    gress.ETA("{s}s"),
    ".",
    maximum=100)
```

**By combination** - Any template can be combined with custom widgets instances.

```python
bar = gress.Bar("Counting: ", gress.Property("current", "{:03}"), " of {maximum} sheep. Ready in {autoeta}.", maximum=100)
```

**By custom widgets within template** - Custom widgets instances can also be registered under unique tag and used
directly within a template.

```python
bar = gress.Bar("Counting: {mycount} of {maximum} sheep. Ready in {autoeta}.", maximum=100)
bar.register("mycount", gress.Property("current", "{:03}"))
```


### Used as iterable
The progress bar can be used directly as an iterable by providing valid source. In such scenario the increment is done
automatically for every iteration call.

```python
# using collection
for i in bar([1,2,3,4,5]):
    do_something()

# using range
for i in bar(range(100)):
    do_something()

# using iterable
items = (i for i in range(100))
for i in bar(items, maximum=100):
    do_something()
```

### Updating the progress manually
Depending on particular situation, different types of manual progress update may be useful. Upon every update the bar
decides whether the displayed progress should be refreshed or not. This can be influenced by the **refresh** argument
of the bar itself.

```python
# by increment
step = 10
for i in range(0, 100, step):
    do_something()
    bar += step

# by increment method
step = 10
for i in range(0, 100, step):
    do_something()
    bar.increase(step)

# to specific value
step = 10
for i in range(0, 100, step):
    do_something()
    bar.update((i+1)*step)
```

### Messaging during the progress
Any message can be writen during processing using the bar **.write()** method. It can be as simple as a single string or
as complex as a combination of multiple widgets. Depending on the **permanent** argument, the message can be displayed
permanently of removed later by next progress update.

```python
bar.write("{time} I should sleep now, so I'm counting slower!")
```

### Finishing the progress
To inform the bar that the progress has finished just call the **finish()** method. This stops the elapsed time to be
increase any further and prints the final state of the progress. This behavior can be modified by providing custom
widgets to be displayed and writen permanently. In case the progress bar is used as iterable, it silently finishes
itself automatically when iteration stops.

```python
bar.finish("{time} All {count} sheep counted in {autotimer} with the average rate of {speed}/s.")
```

## Available Widgets
There are multiple widgets types available covering various aspects of processing from simple count or animated progress
bar up to estimated time of the process to finish. As mentioned above, they can be used as custom instances with
specific settings or many of the predefined widgets can be used directly within a template string.


### Property widget
The Property widget displays specified progress value using given formatting template. Optionally, if unit prefixes are
provided, the value is scaled automatically and corresponding unit prefix is added (e.g. 1500 vs. 1.50 k). There are
predefined prefixes available like *PREFIXES* - typically used for data scaling. Note that the power multiplier can be
specified as well (e.g. 1024 for data).

    name: str
        Name of the progress bar property to show. (E.g. "current", "minimum", "maximum".)
    
    template: str
        Custom template to be used to format the property value (e.g. "{:.2f}").
    
    prefixes: (str,) or None
        Units prefix for each power (e.g. gress.PREFIXES).
    
    step: int
        Multiplier of the power (e.g. 1000 or 1024).

#### Predefined prefix sequences
- **PREFIXES** = ("", "k", "M",  "G",  "T",  "P",  "E",  "Z",  "Y")

#### Predefined simple property widgets
- **{current}** : Property(name="current", template=None)
- **{minimum}** : Property(name="minimum", template=None)
- **{maximum}** : Property(name="maximum", template=None)
- **{min}** : Property(name="minimum", template=None)
- **{max}** : Property(name="maximum", template=None)
- **{count}** : Property(name="current", template="{:.0f}")
- **{percent}** : Property(name="percent", template="{:.0f}")

#### Predefined scaled property widgets
- **{data}** : Property(name="current", template="{:.2f}", prefixes=PREFIXES, step=1024)
- **{dataminimum}** : Property(name="minimum", template="{:.2f}", prefixes=PREFIXES, step=1024)
- **{datamaximum}** : Property(name="maximum", template="{:.2f}", prefixes=PREFIXES, step=1024)
- **{datamin}** : Property(name="minimum", template="{:.2f}", prefixes=PREFIXES, step=1024)
- **{datamax}** : Property(name="maximum", template="{:.2f}", prefixes=PREFIXES, step=1024)
- **{sci}** : Property(name="current", template="{:.2f}", prefixes=PREFIXES, step=1000)
- **{sciminimum}** : Property(name="minimum", template="{:.2f}", prefixes=PREFIXES, step=1000)
- **{scimaximum}** : Property(name="maximum", template="{:.2f}", prefixes=PREFIXES, step=1000)
- **{scimin}** : Property(name="minimum", template="{:.2f}", prefixes=PREFIXES, step=1000)
- **{scimax}** : Property(name="maximum", template="{:.2f}", prefixes=PREFIXES, step=1000)


### Time widget
The Time widget displays current time according to specified template, which should follow the standard datetime
notation (e.g. "%Y-%m-%d %H:%M:%S").

    template: str or None
        Custom template to be used to format the time. The template should use standard
        datetime notation (e.g. "%Y-%m-%d %H:%M:%S"). If set to None, full time is shown.

#### Predefined time widgets
- **{time}** : Time()


### Timer widget
The Timer widget displays current progress elapsed time, according to specified template or formatted automatically as
needed. The template can use "dhms" characters to format individual parts (e.g. "{m:02}:{s:02}"). Optionally, the time
units can be displayed if automatic formatting is used.

    template: str or None
        Custom template to be used to format the time. The template can use "dhms" characters
        to format individual parts (e.g. "{m:02}:{s:02}"). If set to None, remaining time is
        formatted automatically.
    
    units: bool
        If se to True and no template is provided, remaining time is shown with units.

#### Predefined time templates
- **TIME_ABS** = "%Y-%m-%d %H:%M:%S"
- **TIME_DHMS** = "{d}:{h:02}:{m:02}:{s:02}"
- **TIME_HMS** = "{h:02}:{m:02}:{s:02}"
- **TIME_MS** = "{m:02}:{s:02}"
- **TIME_S** = "{s}"
- **TIME_DHMS_U** = "{d}d {h}h {m}m {s}s"
- **TIME_HMS_U** = "{h}h {m}m {s}s"
- **TIME_MS_U** = "{m}m {s}s"
- **TIME_S_U** = "{s}s"

#### Predefined timer widgets
- **{timer}** : Timer(template=TIME_HMS)
- **{autotimer}** : Timer(template=None, units=True)


### ETA widget
The ETA widget displays current progress estimated time of finish, according to specified template or formatted
automatically as needed. If absolute time should be displayed, the template should use the standard datetime notation
(e.g. "%Y-%m-%d %H:%M:%S"). For remaining time the template can use "dhms" characters to format individual parts
(e.g. "{m:02}:{s:02}"). Optionally, the time units can be displayed if automatic formatting is used.

The time is by default calculated using several latest progress updates, unless the adaptive parameter is set to False.
In such case the whole elapsed time and progress is used.

    template: str or None
        Custom template to be used to format the time. For absolute ETA the template
        should use the standard datetime notation (e.g. "%Y-%m-%d %H:%M:%S"). For relative
        ETA the template can use "dhms" characters to format individual parts
        (e.g. "{m:02}:{s:02}"). If set to None, remaining time is formatted automatically.
    
    units: bool
        If se to True and no template is provided, remaining time is shown with units.
    
    absolute: bool
        If set to True, remaining time is shown as the absolute time of expected finish,
        otherwise the remaining time is shown.
    
    adaptive: bool
        If set to True, the speed is calculated from last N updates only, otherwise
        the whole progress is used. Number of updates depends on the progress bar settings.

#### Predefined ETA widgets
- **{eta}** : ETA(template=TIME_HMS, absolute=False, adaptive=True)
- **{autoeta}** : ETA(template=None, units=True, absolute=False, adaptive=True)
- **{abseta"}** : ETA(template=TIME_ABS, absolute=True, adaptive=True)


### Speed widget
The Speed widgets displays current progress speed, according to specified template. Optionally, if unit prefixes are
provided, the value is scaled automatically and corresponding unit prefix is added (e.g. 1.5 MBps). There are predefined
prefixes available like *PREFIXES* - typically used for data scaling. Note that the power multiplier can be specified
as well (e.g. 1024 for data).

The speed is by default calculated using several latest progress updates, unless the adaptive parameter is set to False.
In such case the whole elapsed time and progress is used.

    template: str
        Custom template to be used to format the speed value.
    
    prefixes: (str,) or None
        Units prefix for each power (e.g. gress.PREFIXES).
    
    step: int
        Multiplier of the power (e.g. 1000 or 1024).
    
    adaptive: bool
        If set to True, the speed is calculated from last N updates only, otherwise
        the whole progress is used. Number of updates depends on the progress bar settings.

#### Predefined speed widgets
- **{speed}** : Speed(template="{:.2f}", prefixes=None, adaptive=True)
- **{bps}** : Speed(template="{:.2f}", prefixes=PREFIXES, step=1024, adaptive=True)
- **{dataspeed}** : Speed(template="{:.2f}", prefixes=PREFIXES, step=1024, adaptive=True)
- **{scispeed}** : Speed(template="{:.2f}", prefixes=PREFIXES, step=1000, adaptive=True)


### Gauge widget
The Gauge widget displays current progress as a proportionally filled bar. The characters used can be fully customized
to achieve desired look. If the size is not specified, it fills all available space automatically. In case the parent
progress does not specify the maximum value, the marker character just bounces back a forth instead of filling the bar.

    marker: str
        Character used to show current progress (e.g. "=").
    
    left: str
        Character used for the left edge (e.g. "[").
    
    right: str
        Character used for the right edge (e.g. "]").
    
    fill: str
        Character used to fill remaining space (e.g. "-").
    
    tip: str
        Character used for the progress tip (e.g. ">").
    
    size: int or None
        Desired length of the gauge. If set to None, whole available space will be used.

#### Predefined gauge widgets
- **{gauge}** : Gauge(marker="|", left="|", right="|", fill="-", tip="")
- **{bar}** : Gauge(marker="█", left="", right="", fill="-", tip="")


### Spin widget
The Spin widget displays current progress as animated character. It is defined by a sequence of characters to use, each
update displays the next available character. By setting the widget as relative, available characters are mapped to
cover the whole progress range, otherwise the widget circles through them.

    markers: str
        Individual characters to animate (e.g. "→↘↓↙←↖↑↗" or simply grass.ARROW).
    
    fin: str
        Final character after process finished. If not specified, the last character
        of given markers is used.
    
    relative: bool
        If set to True, characters are distributed equally across full progress.
        If set to False, next character is used for every update.

#### Predefined spin sequences
- **ARROW** = "→↘↓↙←↖↑↗"
- **CIRCLE** = " .oO"
- **DOTS** = " ⡀⡄⡆⡇⣇⣧⣷⣿"
- **FADE** = " ░▒▓█"
- **HBAR** = " ▏▎▍▌▋▊▉█"
- **LINE** = "⎽⎼⎻⎺⎻⎼"
- **MOON** = "◑◒◐◓"
- **PIE** = "○◔◑◕●"
- **PIXEL** = "⣾⣷⣯⣟⡿⢿⣻⣽"
- **SNAKE** = " ▖▌▛█"
- **STAR** = "-\\|/"
- **VBAR** = " ▁▂▃▄▅▆▇█"

#### Predefined spin widgets (cycling)

- **{arrow}** : Spin(markers=ARROW, fin="↑", relative=False)
- **{circle}** : Spin(markers=CIRCLE, relative=False)
- **{dots}** : Spin(markers=DOTS, relative=False)
- **{fade}** : Spin(markers=FADE, relative=False)
- **{hbar}** : Spin(markers=HBAR, relative=False)
- **{line}** : Spin(markers=LINE, relative=False)
- **{moon}** : Spin(markers=MOON, relative=False)
- **{pie}** : Spin(markers=PIE, relative=False)
- **{pixel}** : Spin(markers=PIXEL, fin="⣿", relative=False)
- **{snake}** : Spin(markers=SNAKE, relative=False)
- **{spin}** : Spin(markers=STAR, fin="|", relative=False)
- **{star}** : Spin(markers=STAR, fin="|", relative=False)
- **{vbar}** : Spin(markers=VBAR, relative=False)

#### Predefined spin widgets (relative)

- **{reldots}** : Spin(markers=DOTS, relative=True)
- **{relfade}** : Spin(markers=FADE, relative=True)
- **{relhbar}** : Spin(markers=HBAR, relative=True)
- **{relpie}** : Spin(markers=PIE, relative=True)
- **{relsnake}** : Spin(markers=SNAKE, relative=True)
- **{relvbar}** : Spin(markers=BAR, relative=True)


### Callback widget
The Callback widget provides a special type of widgets to displays custom variables within the progress bar retrieved
by specified callback function. The callback is typically specified as a lambda function with no input parameters,
returning the final formatted custom value.

    callback: callable
        Custom function to be used to retrieve and format the custom value.

### Variable widget
The Variable widget provides a special type of widgets to displays custom variables within the progress bar. Optionally,
the formatting template can be provided to format the value automatically into string.

    value: any
        Current variable value.
    
    template: str
        Custom template to be used to format the value (e.g. "{:.2f}").

## Disclaimer

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
