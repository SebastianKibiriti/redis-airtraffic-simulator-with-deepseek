-- KEYS[1]: aircraft:positions key
-- ARGV[1]: current longitude (string)
-- ARGV[2]: current latitude (string)
-- ARGV[3]: current altitude (string)
-- ARGV[4]: current aircraft ID (string)
local nearby = redis.call('GEORADIUS', KEYS[1], tonumber(ARGV[1]), tonumber(ARGV[2]), 1, 'km', 'WITHDIST')
local conflicts = {}

for i = 1, #nearby, 2 do
    local other_id = nearby[i]
    local distance = tonumber(nearby[i+1])
    local other_alt = tonumber(redis.call('ZSCORE', 'aircraft:altitudes', other_id))
    local alt_diff = math.abs(other_alt - tonumber(ARGV[3]))
    
    if alt_diff < 0.5 and distance < 1.0 then
        table.insert(conflicts, other_id)
    end
end

if #conflicts > 0 then
    redis.call('XADD', 'conflict_alerts', '*', 'trigger_id', ARGV[4], 'conflicts', table.concat(conflicts, ","))
end

return conflicts