#!/usr/bin/env bash

./mcstas-component-to-dom.py  -type=IQE_monitor -category=monitors --base=Monitor --tablebase=MonitorTableBase --newname=QEMonitor --skip-props=filename
./mcstas-component-to-dom.py  -type=Channeled_guide -category=obsolete --newname=ChanneledGuide