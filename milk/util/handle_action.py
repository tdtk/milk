

def action_data2dict(data: str) -> dict:
  res = {}
  for d in data.split("&"):
    kv = d.split("=")
    res[kv[0]] = kv[1]
  return res
