## User Agent Object
The user agent object is found in the [request object](request.md), at [`request.agent`](request.md#agent). It contains all the data AElfi was able to work out about the user, parsed from the user-agent string.

***Note:*** *User agent strings can easily be falsified, so only use this for insecure operations, like redirecting mobile users, not for security uses, unless you know what you're doing.*

#### `browser`
The browser that the user is using is stored in a dictionary including the name, version and engine. The name can be:
- `'Chrome'`
- `'Opera'`
- `'Edge'`
- `'Chrome'`
- `'Safari'`
- `'Firefox'`
- `'MicroSoft Internet Explorer (MSIE)'`

The default is :
```python
{
    'name': '',
    'version': '',
    'engine': {
        'name': '',
        'version': ''
    }
}
```

#### `device`
The brand of the device. Values include:
- `'HTC'`
- `'Samsung'`
- `'Nexus'`
- `'Motorola'`
- `'LG'`
- `'Lumia'`
- `'iPhone'`
- `'iPad'`
- `'Mac'`
- `'Smartphone'`
- `'Computer'`

Defaults to `'Computer'`.

#### `istouch`
Whether AElfi thinks the device is touchscreen. Defaults to `False`.

#### `os`
A dictionary contain the operating system name and version. Default is `{'name': '','version': ''}`.

#### `system`
What architechture the computer is running. Defaults to `'32/64'`.

#### `type`
The type of computer, whether it is `'mobile'`, `'desktop'` or `'tablet'`. Defaults to `'desktop'`.



