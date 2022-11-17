def run(runner):
    val = int(runner.getParams("batch_size"))*3
    runner.publishMetrics("RMSE", val)