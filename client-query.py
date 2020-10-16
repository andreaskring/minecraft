from mcipc.query import Client


with Client('127.0.0.1', 25565) as client:
    basic_stats = client.basic_stats

print(basic_stats)
