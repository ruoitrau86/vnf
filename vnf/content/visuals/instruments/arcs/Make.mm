# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2004  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = vnf
PACKAGE = content/visuals/instruments/arcs


# directory structure

BUILD_DIRS = \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)


#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	ArbitraryDispersionStartPanel.py \
	BeamProfile.py \
	BeamProfileResultsView.py \
	BeamProfileStartPanel.py \
	BeamProfileTableView.py \
	FactoryRoot.py \
	HistogramView.py \
	IQEResolutionComputation.py \
	IQEResolutionResultsView.py \
	IQEResolutionStartPanel.py \
	ResultsViewFactoryBase.py \
	StartPanelFactoryBase.py \
	TableViewFactoryBase.py \
	__init__.py \


export:: export-package-python-modules 


#include doxygen/default.def
# docs: export-doxygen-docs

# version
# $Id: Make.mm 1213 2006-11-18 16:17:08Z linjiao $

# End of file
