# CTFd-Plugins

## Introduction

This repository contains three CTFd plugins, the first allowing unique flags to be added for each team and cheaters to be detected, a plugin allowing solutions to be given once the challenge has been solved and finally a plugin allowing challenges to be hidden and the challenge to be displayed once it has been solved (blackbox).

## Table of contents

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [Plugin 1 : Unique flags](#plugin-1-unique-flags)
- [Plugin 2 : Universal flag submitter](#plugin-2-universal-flag-submitter)
- [Plugin 3 : Writeup](#plugin-3-writeup)
- [Installation](#installation)
- [Update](#update)
- [Support](#support)
- [Credits](#credits)

<!-- TOC end -->

<!-- TOC --><a name="plugin-1-unique-flags"></a>

## Plugin 1 : Unique flags
This plugin allows you to validate a single flag per team, and you can also import the flags with a CSV file. As each team has its own flag, the plugin is also able to detect cheating.
<details>
  <summary>Screenshots</summary>
  
![Batch admin](Screenshots/unique_flags/admin.png)

![Single flag admin](Screenshots/unique_flags/admin-single.png)


![Cheating view](Screenshots/unique_flags/admin-cheating.png)
</details>


<!-- TOC --><a name="plugin-2-universal-flag-submitter"></a>

## Plugin 2 : Universal flag submitter
This plugins will overwrite the default challenge template, and add a way to submit flag trough one forms. This plugin is made for blackbox. An administrator interface is provided to hide challenges from the default interface. Please note that this plugin is not compatible with the requirements and next functions. You need to use Team name generated from the following script `team-generator.py` 

<details>
  <summary>Screenshots</summary>

![Admin view](Screenshots/universal_flag_submitter/admin.png)

![User view](Screenshots/universal_flag_submitter/user.png)
</details>


<!-- TOC --><a name="plugin-3-writeup"></a>

## Plugin 3 : Writeup
This plugin will add a button to report on each challenge by overwriting a template. The user will be able to see the content of the article after solving it.
The administrator has an interface for adding comments to the database. Text can be written in markdown.

<details>
  <summary>Screenshots</summary>

![Admin view](Screenshots/writeup/plugin-admin-markdown.png)

![User link](Screenshots/writeup/plugin-user.png)

![User view](Screenshots/writeup/plugin-user-show.png)

</details>

<!-- TOC --><a name="installation"></a>
## Installation

1. Copy the desired plugin folder to your CTFd plugins folder

```bash
cp CTFd-<Uniques_flags|Universal_flag_submitter|Writeup> plugins/ -r
```
2. Build the docker image
```bash
docker compose build
```

3. Configure secret in .env
```bash
cp .env.example .env
```
Edit the file to insert secret. A python command for generating strong secret is also in the `.env` file.

4. Start the stack
```bash
docker compose up -d
```

Please read the readme file in each folder for specific installation information. Especially for plugins (Universal flag submitter & Unique flag)

<!-- TOC --><a name="update"></a>
## Update

To update CTFd, change the version number modify the Dockerfile

<!-- TOC --><a name="support"></a>
## Support

For questions, support regarding plugins, please open an issue. If you wish to report a security vulnerability, please follow the [security.md](SECURITY.md) guidelines.

## FAQ 

### Where is my data ?

All your data is saved in the `data` folder. 
The data folder use the following structure. If you want to update a plugin, don't forget to rebuild the docker image and delete the redis folder.

```bash
data
├── CTFd
│   ├── logs
│   └── uploads
├── mysql
│   ├── ctfd
│   ├── mysql
│   ├── performance_schema
│   └── sys
└── redis
```

### Is it possible to reset CTFd ?

Yes, you can do this from the administrator interface. However, as it is possible to import challenges, teams and flags, we strongly advise you to archive the data folder and create a new, empty data folder before starting a new installation.


<!-- TOC --><a name="credits"></a>
## Credits

[1] [Isotech42](https://github.com/Isotech42/CTFd-RedHerring) : Cheating monitoring & Part of Unique flags validation