def run(runner):
    val = int(runner.getParams("net_size"))*3
    runner.publishMetric("RMSE", val)