using JSON
using Pkg

# Deamon functions
##################
function write_daemon_file(file::Dict)
    global daemon_file
    while true
        try
            io = open(daemon_file, "w")
            JSON.print(io, file, 2)
            close(io)
            break
        catch e
            @debug("Failed to write to file $(daemon_file))")
        end
        sleep(1)
    end
end

function read_daemon_file()
    global daemon_file
    while true
        try
            io = open(daemon_file, "r")
            file = JSON.parse(io)
            close(io)
            return file
        catch e
            @debug("Failed to read from file $(daemon_file))")
        end
        sleep(1)
    end
    
end

function run_redundancy_removal(file_suffix::String, multi_threaded::Bool)
    global wdir
    global optimizer
    cbco_dir = wdir*"/data_temp/julia_files/cbco_data"

    if multi_threaded & (Threads.nthreads() >= 2)
        @info("Run case $(file_suffix) on $(Threads.nthreads()) threads")
        RedundancyRemoval.run_redundancy_removal(cbco_dir, file_suffix, optimizer, filter_only=true)
    else
        @info("Run case $(file_suffix) single threaded")
        RedundancyRemoval.run_redundancy_removal(cbco_dir, file_suffix, optimizer, parallel=false)
    end
end

function run_redundancy_removal_fbmc_domain(multi_threaded::Bool)
    global wdir
    global optimizer
    cbco_dir = wdir*"/data_temp/julia_files/cbco_data"

    if multi_threaded & (Threads.nthreads() >= 2)
        @info("Run FBMC Domain Reduction on $(Threads.nthreads()) threads")
        RedundancyRemoval.run_redundancy_removal_fbmc_domain(cbco_dir, optimizer, parallel=true)
    else
        @info("Run case single threaded")
        RedundancyRemoval.run_redundancy_removal_fbmc_domain(cbco_dir, optimizer, parallel=false)
    end
end

function run_julia_market_model(redisp_arg::Bool)
    global wdir
    global optimizer

    data_dir = wdir*"/data_temp/julia_files/data/"
    result_dir = wdir*"/data_temp/julia_files/results/"
    if redisp_arg
        @info("Run market model, including redispatch")
    else
        @info("Run market model")
    end
    MarketModel.run_market_model(data_dir, result_dir, optimizer, redispatch=redisp_arg)
    @info("Done with market model.")
end

function set_optimizer(file)
    global gurobi_installed 
    if solver == "Gurobi" && file["chance_constrained"] && gurobi_installed
        @info("Using Gurobi for Chance Constrained Market Model...")
        global optimizer = Gurobi
    elseif  file["chance_constrained"] && !(gurobi_installed)
        @info("Using ECOS for Chance Constrained Market Model...")  
        global optimizer = ECOS
    elseif solver == "Gurobi" && gurobi_installed
        @info("Using Gurobi Solver...")
        global optimizer = Gurobi    
    elseif solver == "ECOS"
        @info("Using ECOS Solver...")
        global optimizer = ECOS
    else
        @info("Using Clp Solver...")
        global optimizer = Clp
    end
end

# Setting everthing up
######################
global julia_package_type = ARGS[1]
global pdir = ARGS[2]
global solver = ARGS[3]
global wdir = pwd()
global daemon_file = pdir*"/daemon_"*julia_package_type*".json"

global gurobi_installed 

if VERSION >= v"1.4"
    isinstalled(pkg::String) = any(x -> x.name == pkg && x.is_direct_dep, values(Pkg.dependencies()))
    gurobi_installed = isinstalled("Gurobi") 
else
   gurobi_installed = "Gurobi" in keys(Pkg.installed()) ? true : false
end

if solver == "Gurobi" && gurobi_installed
    @info("Loading Gurobi...")
    using Gurobi 
elseif solver == "Gurobi" && file["chance_constrained"] && !(gurobi_installed)
    @info("Gurobi not installed. Loading ECOS for CC Formulation...")
    using ECOS
elseif solver == "ECOS"  
    @info("Loading ECOS...")
    using ECOS
else
    @info("Loading Clp...")
    using Clp
end

if julia_package_type == "redundancy_removal"
    using RedundancyRemoval
elseif julia_package_type == "market_model"
    using MarketModel
else
    throw(ArgumentError("No valid argument given"))
end

@info("reading from file $(daemon_file)")
file = read_daemon_file()

# Run the loop
##############
@info("Done with Initialization. Starting daemon process $(file["type"])!")
while true
    local file
    file = read_daemon_file()
    if file["break"]
        @info("EXIT")
        break
    end
    sleep(0.1)
    if file["run"]
        file["run"] = false
        file["processing"] = true
        write_daemon_file(file)
        set_optimizer(file)
        @info("Starting with $(file["type"])")

        if file["type"] == "redundancy_removal"
            multi_threaded = file["multi_threaded"]
            if file["fbmc_domain"]
                run_redundancy_removal_fbmc_domain(multi_threaded)
            else
                file_suffix = file["file_suffix"]
                multi_threaded = file["multi_threaded"]
                run_redundancy_removal(file_suffix, multi_threaded)
            end
        end
        if file["type"] == "market_model"
            global wdir
            redispatch = file["redispatch"]
            data_dir = file["data_dir"]
            run_julia_market_model(redispatch)
        end
        file["processing"] = false
        write_daemon_file(file)
    end
    sleep(0.1)
    if !file["ready"]
        file["ready"] = true
        write_daemon_file(file)
    end
    # println("sleepy")
    sleep(0.1)
end
