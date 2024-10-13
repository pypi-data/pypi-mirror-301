# dvlogger

```
import logging
import dvlogger

dvlogger.setup(level=logging.DEBUG, capture_warnings=True, exception_hook=True, use_tg_handler=False, use_file_handler=False, file_config=None, tg_config=None)
```

```
file_config
    name ['dvlogger_rotating', 'dvlogger_timed', 'dvlogger_basic']
    kind [ROTATING, TIMED, BASIC]
    level [logging.INFO] # TODO - take list of multiple levels to create multiple files

    rotating_size [1e6]
    rotating_count [3]

    timed_when ['midnight']
    timed_interval [1]
    timed_count [5]

    basic_date_format ['%Y_%m_%d_%H_%M%_S_%f']
    basic_put_date [False]
    basic_append [True]

tg_config
    level [ERROR]
    bot_key
    chat_id
    thread_id [None]
```
