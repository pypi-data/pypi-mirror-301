# CmkRedisTools

## Installation

To install the CmkRedisTools package, you can use pip:

```sh
pip install cmk-tools
```
or

```sh
poetry add cmk-tools
```

## Testing

To run tests for CmkRedisTools, use the following command:

```sh
pytest
```

## Example

Here is a simple example of how to use CmkRedisTools:

```python
from cmk_tools import RedisSemaphore, run_with_semaphore

semaphore = RedisSemaphore(
    'redis://localhost:6379/0',
    name="my_semaphore",
    limit=3,            # limit concurrent running task
    timeout=10          # accquire timeout
)

run_with_semaphore(
    your_func,
    func_args,
    func_kwargs,
    execute_when_timeout=True       # execute function if accquired timeout
)
```

For more detailed documentation, email me.
