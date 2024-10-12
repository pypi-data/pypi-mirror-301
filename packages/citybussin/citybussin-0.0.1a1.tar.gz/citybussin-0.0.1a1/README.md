# citybussin

WIP, will eat your underfunded bus

CityBus (of West Lafayette)'s API wrapped up in a Python library


# Usage

Import library and use


## Example

```python
from citybussin import Citybussin
c = Citybussin()

target_route = c.get_route_by_short_name("4B")
target_route_stops = c.get_route_stops(target_route["key"])
target_route_directions = c.get_route_directions(target_route["key"])
target_route_direction = target_route_directions[0]
next_depart_times = c.get_next_depart_times(target_route["key"], target_route_direction["direction"]["key"],
                                            target_route_stops[0]["stopCode"])

import humanize
from datetime import datetime

humanize.naturaltime(datetime.fromisoformat(next_depart_times[0]["estimatedDepartTimeUtc"]))
# 14 minutes from now
```