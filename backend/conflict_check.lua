-- KEYS[1]: aircraft:positions key
-- ARGV[1]: current longitude, ARGV[2]: current latitude
-- ARGV[3]: current altitude, ARGV[4]: current aircraft ID
local nearby = redis.call('GEORADIUS', KEYS[1], ARGV[1], ARGV[2], 1, 'km', 'WITHDIST')
local conflicts = {}
-- GEORADIUS with WITHDIST returns a table of tables, e.g., {{id1, dist1}, {id2, dist2}}.
-- We must iterate through this structure correctly.
for _, item in ipairs(nearby) do
    local other_id = item[1]
    local distance = tonumber(item[2])
    -- Don't check an aircraft against itself.
    if other_id ~= ARGV[4] then
        local other_alt = redis.call('ZSCORE', 'aircraft:altitudes', other_id)
        -- Ensure other_alt is not nil to prevent script errors from inconsistent data.
        if other_alt then
            local alt_diff = math.abs(tonumber(other_alt) - tonumber(ARGV[3]))
            -- Conflict if within 1km horizontally and 1000ft vertically.
            if alt_diff < 1000 and distance < 1.0 then
                table.insert(conflicts, other_id)
            end
        end
    end
end

if #conflicts > 0 then
    redis.call('XADD', 'conflict_alerts', '*', 'trigger_id', ARGV[4], 'conflicts', table.concat(conflicts, ','))
end

return conflicts