import json
import logging
import os
import random
import shutil
import time
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from context import pomato

# pylint: disable-msg=E1101
class TestPomatoVisualization(unittest.TestCase):
    
    def setUp(self):
        wdir = Path.cwd().joinpath("examples")
        self.mato = pomato.POMATO(wdir=wdir, options_file="profiles/nrel118.json",
                                  logging_level=logging.ERROR)
        self.mato.load_data('data_input/nrel_118.zip')
        
        R2_to_R3 = ["bus118", "bus076", "bus077", "bus078", "bus079", 
                    "bus080", "bus081", "bus097", "bus098", "bus099"]
        self.mato.data.nodes.loc[R2_to_R3, "zone"] = "R3"
        # For GeoPLot option 3
        self.mato.data.lines["cb"] = False
        self.mato.data.lines.loc["line001", "cb"] = True  
        
        market_folder = self.mato.wdir.parent.joinpath("tests/test_data/nrel_result/dispatch_market_results")
        redispatch_folder = self.mato.wdir.parent.joinpath("tests/test_data/nrel_result/dispatch_redispatch")
        self.mato.initialize_market_results([market_folder, redispatch_folder])
        self.mato.data.results["dispatch_redispatch"].result_attributes["corresponding_market_result_name"] = "dispatch_market_results"


    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(Path.cwd().joinpath("examples").joinpath("data_temp"), ignore_errors=True)
        shutil.rmtree(Path.cwd().joinpath("examples").joinpath("data_output"), ignore_errors=True)
        shutil.rmtree(Path.cwd().joinpath("examples").joinpath("logs"), ignore_errors=True)

    def test_visualization_generation_plot(self):
        result = self.mato.data.results["dispatch_redispatch"]
        filepath = self.mato.wdir.joinpath("data_output/generation_plot.html")
        self.mato.visualization.create_generation_plot(result, show_plot=False, filepath=filepath)

    def test_visualization_create_installed_capacity_plot(self):
        result = self.mato.data.results["dispatch_redispatch"]
        filepath = self.mato.wdir.joinpath("data_output/capacity_plot.html")
        self.mato.visualization.create_installed_capacity_plot(result, show_plot=False, filepath=filepath)

    def test_visualization_create_storage_plot(self):
        result = self.mato.data.results["dispatch_redispatch"]
        filepath = self.mato.wdir.joinpath("data_output/storage_plot.html")
        self.mato.visualization.create_storage_plot(result, show_plot=False, filepath=filepath)

    def test_visualization_create_generation_overview(self):
        result = self.mato.data.results["dispatch_redispatch"]
        filepath = self.mato.wdir.joinpath("data_output/generation_overview.html")
        self.mato.visualization.create_generation_overview(result, show_plot=False, filepath=filepath)

    def test_fbmc_domain_plot(self):
        folder = self.mato.wdir.parent.joinpath("tests/test_data/nrel_result/scopf_market_results")
        self.mato.initialize_market_results([folder])
        basecase = self.mato.data.results["scopf_market_results"]
        self.mato.options["grid"]["minram"] = 0.1
        self.mato.options["grid"]["sensitivity"] = 0.05
        self.mato.fbmc.calculate_parameters()

        fb_parameters = self.mato.fbmc.create_flowbased_parameters(basecase, gsk_strategy="gmax", reduce=False)
        fbmc_domain = pomato.visualization.FBDomainPlots(self.mato.data, fb_parameters)

        fbmc_domain.generate_flowbased_domain(("R1", "R2"), ["R1", "R3"], "t0001", "nrel")
        fbmc_domain.save_all_domain_plots(self.mato.wdir.joinpath("data_output"), include_ntc=True)
        fbmc_domain.save_all_domain_info(self.mato.wdir.joinpath("data_output"))
        

    def test_geoplot(self):
        result = self.mato.data.results["dispatch_redispatch"]
        filepath = self.mato.wdir.joinpath("data_output/generation_overview.html")
        self.mato.visualization.create_geo_plot(result, show_prices=True, show_redispatch=True, 
                                                show_plot=False, filepath=filepath)

    def test_geoplot_timestep(self):    
        result = self.mato.data.results["dispatch_redispatch"]
        filepath = self.mato.wdir.joinpath("data_output/generation_overview_timestep.html")                                     
        self.mato.visualization.create_geo_plot(result, show_prices=True, show_redispatch=True, 
                                                show_plot=False, timestep=0, filepath=filepath)

    def test_dashboard(self):
        self.mato.start_dashboard()
        time.sleep(5)
        self.mato.stop_dashboard()

if __name__ == '__main__':
    unittest.main()
