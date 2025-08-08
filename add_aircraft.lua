-- KEYS[1]: 2d_positions, KEYS[2]: altitudes
-- ARGV[1]: lng, ARGV[2]: lat, ARGV[3]: alt, ARGV[4]: id
redis.call('GEOADD', KEYS[1], ARGV[1], ARGV[2], ARGV[4])
redis.call('ZADD', KEYS[2], ARGV[3], ARGV[4])
return 1