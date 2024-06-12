[Mesh]
    file = 'cup.e'
  []
    
  [Variables]
    [temperature]
      family = LAGRANGE
      order = FIRST
      initial_condition = 293.15 # Start at room temperature
    []
  []
    
  [Kernels]
    [heat-conduction]
      type = ADHeatConduction
      variable = temperature
    []
    [heat-conduction-dt]
      type = ADHeatConductionTimeDerivative
      variable = temperature
    []
  []
    
  [Functions]
    [temp-func]
      type = ParsedFunction
      value = 'ambient + (temp_zero*exp(-t*constant))'
      vars = 'ambient temp_zero constant'
      vals = '293.15 90.0 0.01'
    []
  []
    
  [BCs]
    [convective]
      type = ADConvectiveHeatFluxBC
      variable = temperature
      boundary = 'convective'
      T_infinity = '293.15'
      heat_transfer_coefficient = 7.8
    []
    [fixed-temp]
      type = ADFunctionDirichletBC
      variable = temperature
      function = 'temp-func'
      boundary = 'fixed-temp'
    []
  []
    
  [Materials]
    [ceramic-density]
      type = ADGenericConstantMaterial
      prop_names = 'density'
      prop_values = '6000'
    []
    [ceramic-conduction]   
      type = ADHeatConductionMaterial
      specific_heat = 850.0
      thermal_conductivity = 30.0
    []
  []
  
  [Postprocessors]
    [handle_temp_max]
      type = ElementExtremeValue
      value_type = max
      variable = 'temperature'
      block = 'handle'
    []
    [handle_temp_min]
      type = ElementExtremeValue
      value_type = min
      variable = 'temperature'
      block = 'handle'
    []
    [handle_temp_avg]
      type = ElementAverageValue
      variable = 'temperature'
      block = 'handle'
    []
  []
  
  [Executioner]
    type = Transient
    solve_type = 'NEWTON'
    petsc_options = '-snes_ksp_ew'
    petsc_options_iname = '-pc_type -sub_pc_type -pc_asm_overlap -ksp_gmres_restart'
    petsc_options_value = 'asm lu 1 101'
    line_search = 'none' 
    nl_abs_tol = 1e-9
    nl_rel_tol = 1e-8
    l_tol = 1e-6
    start_time = 0
    dt = 5
    end_time = 200
  []
  
  [Outputs]
    file_base = ./example/results/ceramic/mug_thermal
    [exodus]
      type = Exodus
    []
    [console]
      type = Console
      output_file = true
    []
    [csv]
      type = CSV
    []
  []
  