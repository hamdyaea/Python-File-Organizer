# Python File Organizer

**Developer:** Hamdy Abou El Anein  
**Contact:** info@daylightlinux.ch  
**License:** GPL v3 (see LICENSE).

A Python 3 command-line organizer that groups regular files into category folders by extension.

**Safety:** Preview is the default. No files move unless you pass `--apply`. Existing destinations are never overwritten; hidden files and symlinks are skipped. Same-filesystem hard links are used to reserve destinations before unlinking originals. Unsupported filesystems may cause a file to be skipped rather than moved. Back up important directories before applying changes.

```sh
python3 organizer.py ~/Downloads
python3 organizer.py ~/Downloads --apply
python3 -m unittest discover -s tests -v
```

The original implementation is preserved on the [old branch](https://github.com/hamdyaea/Python-File-Organizer/tree/old).
