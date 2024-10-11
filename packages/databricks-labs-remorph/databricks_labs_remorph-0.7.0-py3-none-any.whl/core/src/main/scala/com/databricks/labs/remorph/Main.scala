package com.databricks.labs.remorph

case class Payload(command: String, flags: Map[String, String])

object Main extends App with ApplicationContext {
  // scalastyle:off println
  route match {
    case Payload("debug-script", args) =>
      exampleDebugger.debugExample(args("name"), args.get("dialect"))
    case Payload("debug-me", _) =>
      prettyPrinter(workspaceClient.currentUser().me())
    case Payload("debug-coverage", args) =>
      coverageTest.run(os.Path(args("src")), os.Path(args("dst")), args("extractor"))
    case Payload("debug-estimate", args) =>
      val report = estimator(args("source-dialect")).run()
      jsonEstimationReporter(
        os.Path(args("dst")) / s"${now.getEpochSecond}",
        args("preserve-queries").toBoolean,
        report).report()
      args("console-output") match {
        case "true" => consoleEstimationReporter(os.Path(args("dst")) / s"${now.getEpochSecond}", report).report()
      }
    case Payload(command, _) =>
      println(s"Unknown command: $command")
  }

  // parse json from the last CLI argument
  private def route: Payload = {
    val payload = ujson.read(args.last).obj
    val command = payload("command").str
    val flags = payload("flags").obj.mapValues(_.str).toMap
    Payload(command, flags)
  }
}
