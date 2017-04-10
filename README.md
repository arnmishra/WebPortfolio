# WebPortfolio

WebPortfolio is a GUI for SVN projects built for a Programming Studio course at the University of Illinois at Urbana Champaign.

### Usage

First get the configuration files for your SVN repository with the following commands:

```sh
$	svn log --verbose --xml https://subversion.ews.illinois.edu/svn/sp17-cs242/{netid} > svn_log.xml
$	svn list --xml --recursive https://subversion.ews.illinois.edu/svn/sp17-cs242/{netid} > svn_list.xml
```

Move the svn_log.xml and svn_list.xml files to the portfolio/data folder. 

```sh
$  python app.py
```
