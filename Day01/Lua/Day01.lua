local open = io.open

local function readFile(path)
    local file = open(path, "rb")
    if not file then return nil end
    local content = file:read "*a"
    file:close()
    return content
end

local fileContent = readFile("../input.txt")

local lines = {}
for s in fileContent:gmatch("[^\r\n]+") do
    table.insert(lines, s)
end

for i = 1, #lines do
    print(lines[i])
end