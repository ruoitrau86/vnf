

from vnf.components.Form import Form as base


class Form( base ):

    class Inventory( base.Inventory ):

        import pyre.inventory as inv
        id = inv.str( 'id', default = '' )
        id.meta['tip'] = 'A short description'
        
        short_description = inv.str(
            'short_description', default = '' )
        short_description.meta['tip'] = 'A short description'


    def expand(self, form):
        prefix = formactor_action_prefix
        
        p = form.paragraph()
        p.text = ['''<h1>Polycrystal Scattering Intensity Settings</h1>
<p>&nbsp;</p>
<form action="" method="post" enctype="multipart/form-data" name="form1" id="form1">
  <label>Type of Scattering
  <select name="select" id="select">
    <option>Incoherent</option>
    <option>Coherent</option>
  </select>
  </label>
  <p>
    <label>Dynamics Run
    <input type="file" name="fileField" id="fileField" />
    </label>
  </p>
  <p>Q Values
    <label>
    <input name="textfield" type="text" id="textfield" value="-3.0" />
    </label>
    to 
    <label>
    <input name="textfield2" type="text" id="textfield2" value="10" />
    </label>
    incremented by 
    <label>
    <input name="textfield3" type="text" id="textfield3" value="0.1" />
    </label>
  </p>
  <p>Q Shell Width 
    <label>
    <input name="textfield4" type="text" id="textfield4" value="1.0" />
    </label>
  </p>
  <p><span id="sprytextfield1">
    <label>Vectors per shell
    <input name="text1" type="text" id="text1" value="50" />
    </label>
  <span class="textfieldRequiredMsg">A value is required.</span></span></p>
  <p><span id="sprytextfield2">
  <label></label>
  </span> <span id="sprytextfield3"><span class="textfieldRequiredMsg">A value is required.</span></span>
    <label>Units of Q
    <select name="select2" id="select2">
      <option>1/Ang</option>
      <option>1/nm</option>
    </select>
    </label>
  </p>
  <p><span id="sprytextfield4">
    <label>Fourier Transform Window (% Trajectory Length)
    <input name="text3" type="text" id="text3" value="10" />
    </label>
  <span class="textfieldRequiredMsg">A value is required.</span></span></p>
  <p>
    <label>Number of Frequency Points
    <input name="text2" type="text" id="text2" value="1000" />
    </label>