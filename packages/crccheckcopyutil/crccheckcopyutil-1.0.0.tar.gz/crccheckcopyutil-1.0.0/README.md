# Crccheckcopyutil

> [!NOTE]
> Installation is supported only for the following: 
> - Windows

> [!NOTE]
> Development requires a fully configured [Dotfiles](https://github.com/florez-carlos/dotfiles) dev environment <br>

## Table of Contents

* [Installation](#installation)
* [Usage](#usage)
  * [scan](#scan)
  * [verify](#verify) 
* [Development](#development)



## Installation

```bash
python3 -m pip install crccheckcopyutil
```

## Usage

### Scan

-l path to scan<br >
-hl path of the hash file to be saved as .txt<br >

```bash
crccheckcopyutil scan -l C:\PATH\TO\SCAN -hl C:\PATH\TO\HASH.txt
```
This will output a hash.txt file specified in -hl

### Verify

-l path to verify<br >
-hl path of the hash file to compare against<br >

```bash
crccheckcopyutil verify -l C:\PATH\TO\VERIFY -hl C:\PATH\TO\HASH.txt
```

This will output CrcCheckCopy-verification-report.txt in the same dir of the hash file

## Development

> [!NOTE]
> Development requires a fully configured [Dotfiles](https://github.com/florez-carlos/dotfiles) dev environment <br>

```bash
source init.sh
```



