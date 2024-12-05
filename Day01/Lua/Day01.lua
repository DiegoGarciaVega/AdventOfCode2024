-- Open the input file
local file = io.open("../input.txt", "r")
print(file)

-- Initialize lists
local leftList = {}
local rightList = {}

-- Reading file and adding elements to lists
for line in file:lines() do
    local left, right = line:match("(%S+)%s+(%S+)")
    leftList[#leftList + 1] = tonumber(left)
    rightList[#rightList + 1] = tonumber(right)
end

file:close()

-- Sorting the lists
table.sort(leftList)
table.sort(rightList)

-- Calculate totalDistance and similarityScore
local totalDistance, similarityScore = 0, 0
for i = 1, #leftList do
    local leftElement = leftList[i]
    local rightElement = rightList[i]
    totalDistance = totalDistance + math.abs(leftElement - rightElement)

    -- Calculate similarityScore
    local count = 0
    for _, value in ipairs(rightList) do
        if value == leftElement then
            count = count + 1
        end
    end
    similarityScore = similarityScore + count * leftElement
end

-- Print results
print(string.rep("#", 50) .. string.format("\nAdvent of Code 2024\n\t- Day 01\n\t\t★  Result: %d\n\t\t★★ Result: %d\n", totalDistance, similarityScore) .. string.rep("#", 50))