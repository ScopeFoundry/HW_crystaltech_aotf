        ### AOTF #####################################
        #print "Initializing AOTF functionality"
 #       self.dds = CrystalTechDDS(comm="serial", port="COM1", debug=self.HARDWARE_DEBUG)
        
        # Modulation property
#        self.aotf_modulation = self.add_logged_quantity(name="aotf_modulation", dtype=bool, hardware_set_func=self.dds.set_modulation)
#        self.aotf_modulation.updated_value[bool].connect(self.ui.aotf_mod_enable_checkBox.setChecked)
#        self.ui.aotf_mod_enable_checkBox.stateChanged.connect(self.aotf_modulation.update_value)
#        self.aotf_modulation.update_value(True)
        
        # Frequency property
        # TODO:  only works on channel 0!
#        self.aotf_freq = self.add_logged_quantity(name="aotf_freq", 
#                                        dtype=np.float, 
#                                       hardware_read_func=self.dds.get_frequency,
#                                        hardware_set_func=self.dds.set_frequency,
#                                        fmt = '%f')
#        self.aotf_freq.updated_value[float].connect(self.ui.atof_freq_doubleSpinBox.setValue)
#        self.ui.atof_freq_doubleSpinBox.valueChanged[float].connect(self.aotf_freq.update_value)
#        self.ui.aotf_freq_set_lineEdit.returnPressed.connect(self.aotf_freq.update_value)
#        self.aotf_freq.read_from_hardware()
        
        # Power property
        # TODO:  only works on channel 0!
#        self.aotf_power = self.add_logged_quantity(name="aotf_power", 
#                                         dtype=np.int, 
#                                         hardware_read_func=self.dds.get_amplitude,
#                                        hardware_set_func=self.dds.set_amplitude)
#        self.aotf_power.updated_value[float].connect(self.ui.aotf_power_doubleSpinBox.setValue)
#        self.ui.aotf_power_doubleSpinBox.valueChanged.connect(self.aotf_power.update_value)
#        self.aotf_power.read_from_hardware()

from ScopeFoundry import HardwareComponent
try:
    from equipment.crystaltech_dds import CrystalTechDDS
except Exception as err:
    print "Cannot load required modules for CrystalTech DDS (AOTF):", err

class CrystalTechAOTF(HardwareComponent):
    
    def setup(self):
        self.name = 'crystaltech_aotf'
        self.debug = True
        
        # Create logged quantities
        self.modulation_enable = self.add_logged_quantity(
                                       name="modulation_enable",
                                       dtype=bool, 
                                       ro=False)
       
        self.freq0 = self.add_logged_quantity(name="freq0", 
                                        dtype=float, 
                                        unit= "MHz",
                                        vmin= 0,
                                        vmax = 200,
                                        si = False,
                                        fmt = '%f')

        self.pwr0 = self.add_logged_quantity(name="pwr0", 
                                         dtype=int, 
                                         vmin=0,
                                         vmax=1<<16, # 2^16
                                         si=False
                                         )



        #connect GUI
        """
        self.modulation_enable.connect_bidir_to_widget(self.gui.ui.aotf_mod_enable_checkBox)
        self.freq0.connect_bidir_to_widget(self.gui.ui.atof_freq_doubleSpinBox)
#        self.ui.aotf_freq_set_lineEdit.returnPressed.connect(self.aotf_freq.update_value)
        self.pwr0.connect_bidir_to_widget(self.gui.ui.aotf_power_doubleSpinBox)
#        self.ui.aotf_power_doubleSpinBox.valueChanged.connect(self.aotf_power.update_value)
        """
       
    def connect(self):

        #connect to hardware        
        self.dds = CrystalTechDDS(comm="serial", port="COM1", debug=self.debug)
        
        
        # Connect logged quantities to hardware
        self.modulation_enable.hardware_set_func = self.dds.set_modulation
        #self.modulation_enable.hardware_read_func = self.dds.get_ # get_modulation is not defined

        self.freq0.hardware_read_func = self.dds.get_frequency
        self.freq0.hardware_set_func  = self.dds.set_frequency
        
        self.pwr0.hardware_read_func = self.dds.get_amplitude
        self.pwr0.hardware_set_func = self.dds.set_amplitude
#                                         hardware_read_func=self.dds.get_amplitude,
#                                        hardware_set_func=self.dds.set_amplitude)

    def disconnect(self):
        #disconnect logged quantities from hardware
        for lq in self.logged_quantities.values():
            lq.hardware_read_func = None
            lq.hardware_set_func = None
        
        #disconnect hardware
        self.dds.close()
        
        # clean up hardware object
        del self.dds
        