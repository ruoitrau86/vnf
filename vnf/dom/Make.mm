# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = vnf
PACKAGE = dom



BUILD_DIRS = \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
	AbInitio.py \
	ARCS_simple.py \
	Block.py \
	BvKModel.py \
	BvKComputation.py \
	Computation.py \
	Crystal.py \
	Cylinder.py \
	DbObject.py \
	DetectorSystem_fromXML.py \
	Disordered.py \
	Geometer.py \
	GulpScatteringKernel.py \
	IDFPhononDispersion.py \
	Instrument.py \
	IQMonitor.py \
	IQEMonitor.py \
	Job.py \
	MatterBase.py \
	MonochromaticSource.py \
	NeutronComponent.py \
	NeutronExperiment.py \
	OwnedObject.py \
	PhononDispersion.py \
	PolyCrystal.py \
	PolyXtalCoherentPhononScatteringKernel.py \
	ReferenceSet.py \
	SANS_NG7.py \
	SANSSphereModelKernel.py \
	Sample.py \
	SampleAssembly.py \
	SampleComponent.py \
	SampleEnvironment.py \
	Scatterer.py \
	ScattererExample.py \
	ScatteringKernel.py \
	Server.py \
	Shape.py \
	SimulationResult.py \
	SingleCrystal.py \
	Table.py \
	User.py \
	idgenerator.py \
	registry.py \
	_all_tables.py \
	_geometer.py \
	_hidden_tables.py \
	_referenceset.py \
	__init__.py \



export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $

# End of file
