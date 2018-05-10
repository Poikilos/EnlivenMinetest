#!/bin/sh
#du -hsx * | sort -rh | head -10

#including hidden, but excluding . and ..:
du -hsx .[^.]* * | sort -rh | head -10

#see also /var/lib/logrotate for possible HUGE files if logrotate malfunctions
