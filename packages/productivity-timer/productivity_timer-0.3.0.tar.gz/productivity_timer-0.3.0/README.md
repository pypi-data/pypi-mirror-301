
# Productivity-Timer

**Productivity-Timer** is a Python library for managing multiple timers, one for each specified individual. It allows starting, stopping, pausing, resuming, resetting, and retrieving elapsed times for timers on a per-person basis. The library also supports optional timeouts, so timers can automatically stop after reaching a specified duration.

## Features

- Start, stop, pause, resume, and reset individual timers.
- Track multiple timers for different individuals.
- Optional timeout support for automatic stopping.
- Retrieve formatted elapsed times for each person.
- Stop and reset all timers with a single command.

## Installation

To install **Productivity-Timer**, use `pip`:

```bash
pip install productivity-timer 
```

## Usage

### Importing the Library

```python
from productivity_timer import ProductivityTimer
```

### Quick Start

```python
from productivity_timer import ProductivityTimer

timer = ProductivityTimer()

timer.start("Abhishek", timeout=10) 

timer.start("Ram")

timer.pause("Abhishek")  

timer.resume("Abhishek")

timer.stop("Ram")

print(f"Elapsed time for Abhishek: {timer.get_elapsed_time('Abhishek', formatted=True)}")

timer.stop_all()

print(timer)
```

### Available Functions

- **`start(person, timeout=None)`**  
  Starts a timer for the specified person. If a timer for this person already exists, it resumes the timer. The `timeout` argument sets a maximum duration for the timer (in seconds).

- **`stop(person)`**  
  Stops the timer for the specified person and updates the total elapsed time.

- **`pause(person)`**  
  Pauses the timer for the specified person without resetting the elapsed time. The timer can be resumed later.

- **`resume(person)`**  
  Resumes a paused timer for the specified person.

- **`reset(person)`**  
  Resets the timer for the specified person to zero, clearing any elapsed time.

- **`get_elapsed_time(person, formatted=False)`**  
  Returns the elapsed time for the specified person. If `formatted=True`, the time is returned as a formatted string in `HH:MM:SS`.

- **`get_all_elapsed_times(formatted=False)`**  
  Returns a dictionary of elapsed times for all tracked persons. If `formatted=True`, times are formatted in `HH:MM:SS`.

- **`stop_all()`**  
  Stops all active timers.

- **`reset_all()`**  
  Resets all timers, clearing any elapsed times.

- **`check_timeouts()`**  
  Checks each timer against its timeout value (if any). If a timer's elapsed time exceeds its timeout, the timer is automatically stopped.

### Examples

#### Setting Up a Timer with a Timeout

```python
timer.start("Abhishek", timeout=30)  
```

#### Checking and Stopping All Active Timers

```python
timer.stop_all()
```

#### Formatting Elapsed Time

```python
formatted_time = timer.get_elapsed_time("Abhishek", formatted=True)
print(f"Elapsed time for Abhishek: {formatted_time}")
```

### Contributing

Contributions are welcome! If you would like to report issues, suggest new features, or contribute code, please create a pull request or open an issue on the GitHub repository.
