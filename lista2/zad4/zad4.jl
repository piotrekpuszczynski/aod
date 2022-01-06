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
    if last(dir, 4) != "zad4"
        dir = string(dir, "/zad4")
    end

    open("$dir/data.txt") do f
        m = parse(Int, readline(f))
        n = parse(Int, readline(f))
        k = parse(Int, readline(f))

        c = parse(Int, readline(f))
        containers = Array{Int}(UndefInitializer(), c, 2)
        for i in 1:c
            line = parse.(Int, split(readline(f), " "))
            if length(line) != 2
                return Nothinig, Nothing
            end

            containers[i, 1] = line[1]
            containers[i, 2] = line[2]
        end

        return m, n, k, c, containers
    end
end

function getRange(i, j, m, n, k)
    x = zeros(Int, (k * 2 + 1)^2)
    y = zeros(Int, (k * 2 + 1)^2)

    counter = 1
    for l in -k:k
        for o in -k:k
            if !(i + l < 1 || i + l > m || j + o < 1 || j + o > n)
                x[counter] = i + l
                y[counter] = j + o
            else
                x[counter] = i
                y[counter] = j
            end
            counter += 1
        end
    end

    return x, y, (k * 2 + 1)^2
end

function main()
    data = readData()
    if data[1] == Nothing
        println("invalid data")
        return
    end

    m = data[1]
    M = ["m$i" for i in 1:m]
    n = data[2]
    N = ["n$i" for i in 1:n]
    k = data[3]
    c = data[4]
    containers = data[5]

    isContainer = Array{Int}(UndefInitializer(), n, m)
    for i in 1:n
        for j in 1:m
            isContainer[i, j] = 0
        end
    end
    for i in 1:c
        isContainer[containers[i, 1], containers[i, 2]] = 1
    end

    ranges = Array{Int}(UndefInitializer(), n, m)
    for i in 1:n
        for j in 1:m
            if isContainer[i, j] == 1
                ranges[i, j] = 0
                continue
            end
            r = 0
            for l in -k:k
                for o in -k:k
                    if l == 0 && o == 0
                        continue
                    end
                    try 
                        if isContainer[i + l , j + o] == 1
                            r += 1
                        end
                    catch LoadError end
                end
            end
            ranges[i, j] = r
        end
    end
    
    model = Model(GLPK.Optimizer)
    @variable(model, 0 <= x[N, M] <= 1, Int)
    @objective(model, Min, sum(x[i, j] for i in N, j in M))
    
    @constraint(model, sum(x[N[j], M[i]] * ranges[j, i] for i in 1:m, j in 1:n) >= c)

    for i in 1:c
        r = getRange(containers[i, 1], containers[i, 2], n, m, k)
        @constraint(model, sum(x[N[r[1][j]], M[r[2][j]]] for j in 1:r[3]) >= 1)
    end
    
    optimize!(model)

    if string(termination_status(model)) != "OPTIMAL"
        print("Cannot find optimal solution")
    else
        printResult(M, N, value.(x))
        println("cost: ", objective_value(model))
    end

end

main()
