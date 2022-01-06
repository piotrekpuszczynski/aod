using JuMP
using GLPK
using PrettyTables

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
    if last(dir, 4) != "zad2"
        dir = string(dir, "/zad2")
    end
    
    open("$dir/data.txt") do f
 
        n = parse(Int, readline(f))
        cities = ["City $i" for i in 1:n]
        m = parse(Int, readline(f))
        
        a = Array{Int}(UndefInitializer(), m, 4)
        for i in 1:m

            line = parse.(Int, split(readline(f), " "))
            if length(line) != 4
                return Nothing, Nothing
            end

            for j in 1:length(line)
                a[i, j] = line[j]
            end
        end
        line = parse.(Int, split(readline(f), " "))
        s = line[1]
        d = line[2]

        t = parse(Int, readline(f))

        return n, cities, m, a, s, d, t
    end
end


function main()
    data = readData()
    if data[1] == Nothing
        println("invalid data")
        return
    end

    n = data[1]
    cities = data[2]
    m = data[3]
    arcs = data[4]
    source = data[5]
    destination = data[6]
    time = data[7]

    edgeExist = Dict()
    costsDict = Dict()
    timesDict = Dict()
    for i in cities
        for j in cities
            edgeExist[i, j] = 0
            costsDict[i, j] = 0
            timesDict[i, j] = 0
        end
    end
    for i in 1:m
        edgeExist[cities[arcs[i, 1]], cities[arcs[i, 2]]] = 1
        costsDict[cities[arcs[i, 1]], cities[arcs[i, 2]]] = arcs[i, 3]
        timesDict[cities[arcs[i, 1]], cities[arcs[i, 2]]] = arcs[i, 4]
    end

    model = Model(GLPK.Optimizer)
    @variable(model, 0 <= x[cities, cities] <= 1, Int)
    @objective(model, Min, sum(costsDict[i, j] * x[i, j] for i in cities, j in cities))

    for i in 1:n
        if i == source
            @constraint(model, sum(edgeExist[cities[i], j] * x[cities[i], j] - edgeExist[j, cities[i]] * x[j, cities[i]] for j in cities) == 1)
        elseif i == destination
            @constraint(model, sum(edgeExist[cities[i], j] * x[cities[i], j] - edgeExist[j, cities[i]] * x[j, cities[i]] for j in cities) == -1)
        else
            @constraint(model, sum(edgeExist[cities[i], j] * x[cities[i], j] - edgeExist[j, cities[i]] * x[j, cities[i]] for j in cities) == 0)
        end
    end
    @constraint(model, sum(timesDict[i, j] * x[i, j] for i in cities, j in cities) <= time)
    
    optimize!(model)

    if string(termination_status(model)) != "OPTIMAL"
        print("Cannot find optimal solution")
    else
        printResult(cities, cities, value.(x))
        println("cost: ", objective_value(model))
    end
end

main()