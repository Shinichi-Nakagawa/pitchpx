====================
pitchpx
====================

Tools for Acquiring MLBAM Gameday dataset

Requirement
====================

python 3.3+(don't know about version < 3.2, sorry)

Install
====================

    $ pip install pitchpx

Usage
====================

------------------------------
download(MLBAM dataset)
------------------------------

    $ pitchpx [-s, --start <from 8-digit-datetime(YYYYMMDD)>] [-e, --end <to 8-digit-datetime(YYYYMMDD)>] [-o, --output <download file path>]

    -s, --start       : Start Day(YYYYMMDD)

    -e, --end         : End Day(YYYYMMDD)

    -o, --output      : Output directory(default:".")

    -help             : pitchpx command help


License
====================

MIT License http://opensource.org/licenses/MIT

Dataset
====================

MLBAM Gameday http://gd2.mlb.com/components/

copyright http://gd2.mlb.com/components/copyright.txt