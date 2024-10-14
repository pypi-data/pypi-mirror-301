# rsyncer

Simple backup command. Uses `rsync` and `ssh`, with your `ssh` configs.

Need to write `.logs` for it to log.

Dependencies:
- `rsync`
- `ssh`

## Example Config

Default location in `~/.config/rsyncer.toml`.

```
[sources]
[sources.hostname] # for remote sources
paths = ["/path/to/dir/to/backup", "/different/path/to/another/dir", "/a/third/path/etc"]

[sources.local] # for local sources
paths = ["/path/to/dir/to/backup", "/different/path/to/another/dir", "/a/third/path/etc"]

[destinations]
[destinations.hostname]
path = "/path/on/host"

[frequency]
frequencies = ["daily", "weekly", "monthly"] # allowed are dailly, weekly, and monthly

[log]
path = "~/.logs/rsyncer.log"
```

## Usage

## For Development

To install locally for testing:

```
source pyenv/bin/activate
pip install -e .
```


