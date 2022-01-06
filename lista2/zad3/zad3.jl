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
    if last(dir, 4) != "zad3"
        dir = string(dir, "/zad3")
    end

    open("$dir/data.txt") do f
 
        s = parse(Int, readline(f))
        shifts = ["Shift $i" for i in 1:s]
        d = parse(Int, readline(f))
        districts = ["District $i" for i in 1:d]

        min = Array{Int}(UndefInitializer(), d, s)
        max = Array{Int}(UndefInitializer(), d, s)

        for i in 1:d
            line = parse.(Int, split(readline(f), " "))
            if length(line) != s
                return Nothing, Nothing
            end

            for j in 1:length(line)
                min[i, j] = line[j]
            end
        end
        readline(f)
        for i in 1:d
            line = parse.(Int, split(readline(f), " "))
            if length(line) != s
                return Nothing, Nothing
            end

            for j in 1:length(line)
                max[i, j] = line[j]
            end
        end
        readline(f)
        minShifts = parse.(Int, split(readline(f), " "))
        minDistricts = parse.(Int, split(readline(f), " "))

        if length(minShifts) != s || length(minDistricts) != d
            return Nothing, Nothing
        end

        return s, shifts, d, districts, min, max, minShifts, minDistricts
    end
end

function main()
    data = readData()
    if data[1] == Nothing
        println("invalid data")
        return
    end

    s = data[1]
    shifts = data[2]
    d = data[3]
    districts = data[4]
    min = data[5]
    max = data[6]
    minShifts = data[7]
    minDistricts = data[8]
    
    minDict = Dict()
    maxDict = Dict()
    for i in 1:s
        for j in 1:d
            minDict[districts[j], shifts[i]] = min[j, i]
            maxDict[districts[j], shifts[i]] = max[j, i]
        end
    end

    model = Model(GLPK.Optimizer)
    @variable(model, 0 <= x[districts, shifts], Int)
    @objective(model, Min, sum(x[i, j] for i in districts, j in shifts))

    for i in 1:s
        @constraint(model, sum(x[districts[j], shifts[i]] - x[districts[j], shifts[i]] for j in 1:d) == 0)
    end
    for i in districts
        for j in shifts
            @constraint(model, x[i, j] >= minDict[i, j])
            @constraint(model, x[i, j] <= maxDict[i, j])
        end
    end
    for i in 1:s
        @constraint(model, sum(x[j, shifts[i]] for j in districts) >= minShifts[i])
    end
    for i in 1:d
        @constraint(model, sum(x[districts[i], j] for j in shifts) >= minDistricts[i])
    end

    optimize!(model)

    if string(termination_status(model)) != "OPTIMAL"
        print("Cannot find optimal solution")
    else
        printResult(shifts, districts, value.(x))
        println("cost: ", objective_value(model))
    end
end

main()