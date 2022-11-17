def run(runner):
    val = int(runner.getParams("net_size"))*3
    print("here")
    runner.publishMetric("RMSE", val)