# Moodle API Client

> This project is not endorsed by Moodle but developed independently

Developed with [`tiny-api-client`][tiny-api-client]

This library is developed for [Blackboard Sync][bbsync].

```python
from moodle import MoodleSession

session = MoodleSession('https://sandbox.moodledemo.net/', token=...)
session.core_webservice_get_site_info()
```


## Installation

```bash
pip install moods
```



## License

[![License: GPL  v2.1][license-shield]][gnu]

This software is distributed under the [General Public License v2][license],
more information available at the [Free Software Foundation][gnu].


<!-- LINKS -->

[tiny-api-client]: https://pypi.org/project/tiny-api-client
[bbsync]: https://github.com/sanjacob/BlackboardSync


<!-- LICENSE -->

[license]: LICENSE "General Public License v2"
[gnu]: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html "Free Software Foundation"
[license-shield]: https://img.shields.io/github/license/sanjacob/moods


<!-- SHIELD LINKS -->

[pypi]: https://pypi.org/project/moods


<!-- SHIELDS -->

[pypi-shield]: https://img.shields.io/pypi/v/moods
[build-shield]: https://img.shields.io/github/actions/workflow/status/sanjacob/moods/build.yml?branch=master
[docs-shield]: https://img.shields.io/readthedocs/moods
