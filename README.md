# HardnestedRecovery

Program recovers keys from collected authorization challenges (nonces).
You can collect nonces on Flipper Zero with the NFC app using [PR 3822](https://github.com/flipperdevices/flipperzero-firmware/pull/3822)

This Repo contains a statically compiled binary of HardnestedRecovery as well as the script to build it for convenience.


## Building

First, install dependencies (Ubuntu):

`sudo apt update;sudo apt install -y build-essential liblzma-dev p7zip-full`

or on Gentoo install the packages `app-arch/lzma app-arch/7zip`

`sudo emerge --ask app-arch/lzma app-arch/7zip`

Then compile the program:

`make`

or Run the compile script and check the **Compiled** Directory afterwards.

```bash
$ chmod +x "Build Static Hardnested.sh"
$ ./"Build Static Hardnested.sh"
```

## Usage

First, Download the binary from [the release section](https://github.com/GhostNaix/HardnestedRecovery/releases) or Build it your self using the script or manually (Refer to the Building Section if you wish to compile your own. If you cannot compile your own, you may download it from [the release section](https://github.com/GhostNaix/HardnestedRecovery/releases).)

Using qFlipper or the Flipper Mobile App, download the nonces stored at (/ext/)nfc/.nested.log. Then recover the keys by running the program with the path to .nested.log on your computer:

### Self Compiled
If you compiled it yourself then use the following command.

```bash
$ chmod +x hardnested_main
$ ./hardnested_main .nested.log
```

### Downloaded Binary
If you downloaded the binaries from [the release section](https://github.com/GhostNaix/HardnestedRecovery/releases) then use the following command.

```bash
$ chmod +x hardnested_linux_64bit
$ ./hardnested_linux_64bit .nested.log
```

## Example


```
$ ./hardnested_main .nested.log
[=] Hardnested attack starting...
[=] ---------+---------+---------------------------------------------------------+-----------------+-------
[=]          |         |                                                         | Expected to brute force
[=]  Time    | #nonces | Activity                                                | #states         | time
[=] ---------+---------+---------------------------------------------------------+-----------------+-------
[=]        0 |       0 | Start using 8 threads                                   |                 |
[=]        0 |       0 | Brute force benchmark: 124 million (2^26.9) keys/s      | 140737488355328 |   13d
[=]        1 |       0 | Using 235 precalculated bitflip state tables            | 140737488355328 |   13d
[=]       26 |     256 | Loading nonces from file                                |       641827520 |    5s
[=]       42 |     512 | Loading nonces from file                                |       216530400 |    2s
[=]       51 |     768 | Loading nonces from file                                |       216530400 |    2s
[=]       54 |    1024 | Loading nonces from file                                |       216530400 |    2s
[=]       60 |    1051 | Apply Sum property. Sum(a0) = 120                       |        32340672 |    0s
[=]       60 |    1051 | (Ignoring Sum(a8) properties)                           |        32340672 |    0s
[=]       63 |    1051 | Brute force phase completed.  Key found: A0A1A2A3A4A5   |               0 |    0s
Key found for UID: aabbccdd, Sector: 1, Key type: A: a0a1a2a3a4a5
```

Copy each found key to the user dictionary on your Flipper device at (/ext/)nfc/assets/mf_classic_dict_user.nfc and re-read your tag using the NFC app.
