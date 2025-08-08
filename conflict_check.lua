-- KEYS[1]: aircraft:positions
-- ARGV[1]: longitude, ARGV[2]: latitude, ARGV[3]: altitude, ARGV[4]: aircraft_id
local nearby = redis.call('GEORADIUS', KEYS[1], ARGV[1], ARGV[2], 1, 'km', 'WITHCOORD')
for i = 1, #nearby, 2 do
  local other_id = nearby[i]
  local other_alt = redis.call('ZSCORE', 'aircraft:altitudes', other_id)
  if math.abs(other_alt - ARGV[3]) < 1000 then
    redis.call('XADD', 'conflict_alerts', '*', 'aircraft1', ARGV[4], 'aircraft2', other_id)
  end
end