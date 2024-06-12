# Writeup

This plugin lets you add solutions to your challenges.

# Installation

1. Copy the plugins to CTFd's plugin folder
2. Create your own challenges
3. Go to the plugin -> Writeup -> Create your writeup

Done.

It is possible to deactivate the plugin, but the CTFd server must be restarted for the changes to take effect.

# Known issues / Possible improvements
- Issues - In the writeup editing form, the ability to add images is missing (there's a js error). (Issue [#2545](https://github.com/CTFd/CTFd/issues/2545))
- Improvement - Don't reload the page, but rather interact with the API, which would return JSON.