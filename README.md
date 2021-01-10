# vol_moe-downloader

This tool is used to download comics from [vol.moe](https://vol.moe)

**Bugs may exist, use at your own risks**

## Requirement

You must first login your account in a browser, and extract following cookies from your browser:

    - VOLSESS
    - VOLSKEY
    - VLIBSID

## Configuration

``` yaml
account:
  VOLSKEY: "" # your VOLSKEY
  VOLSESS: "" # your VOLSESS
  VLIBSID: "" # your VLIBSID

# browser UA
ua: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"

# the file format, `mobi` or `epub`
type: "epub"

# the directory to store files, can be either absolute or relative
download_path: "./download"

# limits the bandwidth to be used in one day if you dont want to use your mothly
# bandwidth all at once
daily_limit: 99999
```

## Histroy

This file stores all the books have been downloaded, or you can add your own. The file logged here will be skipped.

``` yaml
進擊的巨人: # the name of the book
- 第 00 卷 # the name of each volume
- 第 01 卷
- 第 02 卷
- 第 03 卷
- 第 04 卷
- 第 05 卷
- 第 06 卷
- 第 07 卷
- 第 08 卷
- 第 09 卷
- 第 10 卷
- 第 11 卷
- 第 12 卷
- 第 13 卷
- 第 14 卷
- 第 15 卷
- 公式書-抗Inside
- 第 123-126 話
五等分的花嫁: all # `all` means the whole book will be skipped, or all the volumes have been downloaded and the book is ended.
```