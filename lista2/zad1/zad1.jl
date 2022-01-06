using JuMP
using GLPK
using PrettyTables

function getDifference(companiesResources, airportsRequirements)
    difference = 0
    for i in companiesResources
       difference += i
    end
    for i in airportsRequirements
        difference -= i
    end
    return difference
end

function printResult(companies, airports, x)
    result = Array{String, 2}(undef, length(airports) + 1, length(companies) + 1)
    result[1, 1] = " "
    for i in 1:length(companies)
        result[1, i + 1] = companies[i]
    end
    for i in 1:length(airports)
        result[i + 1, 1] = airports[i]
        for j in 1:length(companies)
            result[i + 1, j + 1] = string(value(x[airports[i], companies[j]]))
        end
    end
    pretty_table(result)
end

function readData()
    dir = pwd()
    if last(dir, 4) != "zad1"
        dir = string(dir, "/zad1")
    end
    
    open("$dir/data.txt") do f
 
        companiesResources = parse.(Int, split(readline(f), " "))
        companies = ["Company $i" for i in 1:length(companiesResources)]

        airportsRequirements = parse.(Int, split(string(readline(f), " 0"), " "))
        airportsRequirements[length(airportsRequirements)] = getDifference(companiesResources, airportsRequirements)
        airports = Array{String}(UndefInitializer(), length(airportsRequirements))
        for i in 1:length(airportsRequirements) - 1
            airports[i] = "Airport $i"
        end
        airports[length(airportsRequirements)] = "Bin"

        costs = Array{Int}(UndefInitializer(), length(airportsRequirements), length(companiesResources))

        for i in 1:length(airportsRequirements) - 1
            if eof(f)
                return Nothing, Nothing
            end
            line = parse.(Int, split(readline(f), " "))
            if length(line) != length(companiesResources)
                return Nothing, Nothing
            end
            for j in 1:length(companiesResources)
                costs[i, j] = line[j]
            end
        end

        for j in 1:length(companiesResources)
            costs[length(airportsRequirements), j] = 0
        end

        return companies, companiesResources, airports, airportsRequirements, costs
    end
end

function main()
    data = readData()
    if data[1] == Nothing
        println("invalid data")
        return
    end

    companies = data[1]
    companiesResources = data[2]
    airports = data[3]
    airportsRequirements = data[4]
    costs = data[5]

    airportsDict = Dict(zip(airports, airportsRequirements))
    companiesDict = Dict(zip(companies, companiesResources))

    costsDict = Dict()
    for i in 1:length(airports)
        for j in 1:length(companies)
            costsDict[airports[i], companies[j]] = costs[i, j]
        end
    end

    model = Model(GLPK.Optimizer)
    @variable(model, x[airports, companies] >= 0)
    @objective(model, Min, sum(costsDict[i, j] * x[i, j] for i in airports, j in companies))

    for i in airports
        @constraint(model, sum(x[i, j] for j in companies) == airportsDict[i])
    end
    for j in companies
        @constraint(model, sum(x[i, j] for i in airports) == companiesDict[j])
    end

    optimize!(model)

    if string(termination_status(model)) != "OPTIMAL"
        print("Cannot find optimal solution")
    else
        printResult(companies, airports, value.(x))
        println("cost: ", objective_value(model))
    end
end

main()
