<?xml version="1.0"?>
<!--
! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!
!
! {LicenseText}
!
! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-->


<!DOCTYPE inventory>

<inventory>

  <component name='main'>
    <property name='actor'>materialsimulationwizard</property> 
    <property name='routine'>onSelect</property>  
    <property name='actor.form-received.kernel'>gulp</property>
    <property name='materialsimulationwizard.form-received'>selectSimulationEngine</property>
    <property name="home">http://trueblue.caltech.edu/vnf/</property>
    <property name="cgi-home">http://trueblue.caltech.edu/cgi-bin/vnf/main.cgi</property>
    <component name="materialsimulationwizard">
            <property name="form-received">selectSimulationEngine</property>
            <component name="selectSimulationEngine">
                <property name="kernel">gulp</property>
     		</component>
    </component>
    <component name='sentry'>
    	<property name='username'>demo</property>
    	<property name='passwd'>demo</property>
    </component>
  </component>

</inventory>


<!-- version-->
<!-- $Id$-->

<!-- Generated automatically by XMLMill on Fri Apr  4 10:17:11 2008-->

<!-- End of file -->
