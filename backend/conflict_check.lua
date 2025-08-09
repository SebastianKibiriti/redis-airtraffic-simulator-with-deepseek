-- KEYS[1]: aircraft:positions key
-- ARGV[1]: current longitude, ARGV[2]: current latitude
-- ARGV[3]: current altitude, ARGV[4]: current aircraft ID
local nearby = redis.call('GEORADIUS', KEYS[1], ARGV[1], ARGV[2], 1, 'km', 'WITHDIST')
local conflicts = {}

for i = 1, #nearby, 2 do
    local other_id = nearby[i]
    local distance = tonumber(nearby[i+1])
    local other_alt = redis.call('ZSCORE', 'aircraft:altitudes', other_id)
    local alt_diff = math.abs(tonumber(other_alt) - tonumber(ARGV[3]))

    if alt_diff < 0.5 and distance < 1.0 then
        table.insert(conflicts, other_id)
    end
end

if #conflicts > 0 then
    redis.call('XADD', 'conflict_alerts', '*', 'trigger_id', ARGV[4], 'conflicts', table.concat(conflicts, ','))
end

return conflicts