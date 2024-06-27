import simvue
import multiparser
import multiprocessing
import os

class WrappedRun(simvue.Run):
    
    def pre_simulation(self):
        self._trigger = multiprocessing.Event()

        if not self._simvue:
            self._error("Run must be initialized before launching the simulation.")
            return False

    def during_simulation(self):
        pass

    def post_simulation(self):
        pass 

    def launch(self):
        self.pre_simulation()
        
        # Start an instance of the file monitor, to keep track of log and results files
        with multiparser.FileMonitor(
            termination_trigger=self._trigger,
        ) as self.file_monitor:
            
            self.during_simulation()
            self.file_monitor.run()
        
        self.post_simulation()