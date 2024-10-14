from genlab_ai_game_util import RedisClient

if __name__ == '__main__':
    k = '__python_test__'
    v = 'value'
    mapping = dict(key1="value1", key2="value2")
    redisClient = RedisClient(host='43.138.239.86', port=7000, password='B8J0fg5589HG9g56', socket_timeout=3,
                              socket_connect_timeout=3)
    # print(redisClient.set_kv(k, v, 10))
    # print(redisClient.get_kv(k))
    print(redisClient.set_hash(k, mapping))
    print(redisClient.get_hash_all(k))
    print(redisClient.exists(k))
    print(redisClient.get_hash_by_key(k, 'key1'))
    print(redisClient.del_hash_by_key(k, 'key2'))
    print(redisClient.inc("__python_test__inc__"))
    print(redisClient.get_kv("__python_test__inc__"))
    redisClient.disconnect()