package ingestor

import net.liftweb.json._

import kafka.serializer.StringDecoder

import org.apache.log4j.{Level, Logger}

import org.apache.spark.streaming.dstream.{DStream, InputDStream}
import org.apache.spark.streaming.kafka.KafkaUtils
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._

import kafkapool._

/**
 * Produces messages for a single topic in Kafka by ingesting an input
 * stream of UTM client server publication service.
 *
 * Usage: Ingestor <brokers> <conflict> <debug>
 *    <brokers> is a list of one or more Kafka brokers; e.g., "localhost:9092"
 *    <conflict> is a Kafka topic to produce conflict messages for; e.g., "conflict"
 *    <debug> is a flag for debug mode (verbosity); e.g., "false"
 *
 *  Example:
 *    `$ Ingestor broker1-host:port,broker2-host:port topic false`
 *
 *  Server startup:
 *    Kafka uses ZooKeeper so start a ZooKeeper server if you don't already
 *    have one. Use the convenience script packaged with kafka to get a quick-
 *    and-dirty single-node ZooKeeper instance.
 *
 *    From the Kafka root, run
 *      `$ bin/zookeeper-server-start.sh config/zookeeper.properties`.
 *
 *    Now start the Kafka server by running
 *      `$ bin/kafka-server-start.sh config/server.properties`.
 *
 *    Once these two servers have been started up, you can start Ingestor. To
 *    verify that messages are being sent, you can start a command line
 *    consumer that will dump out messages to standard output as follows.
 *      `$ bin/kafka-console-consumer.sh --zookeeper <broker> --topic <topic>`
 */
object Ingestor {
  def main(args: Array[String]): Unit = {
    if (args.length < 3) {
      System.err.println(s"""
        |Usage: Ingestor <brokers> <conflict> <debug>
        |  <brokers> is a list of one or more Kafka brokers
        |  <conflict> is a Kafka topic to produce formatted conflict messages for
        |  <debug> is a flag for debug mode (verbosity)
        |
        """.stripMargin)
      System.exit(1)
    }

    val Array(brokers, conflict, debug) = args

    if (debug == "false") {
      Logger.getLogger("org").setLevel(Level.WARN)
    }
    // local StreamingContext with 2 working threads and batch interval of 1 second
    val conf = new SparkConf()
      .setAppName("DroneSimulator")
      .setMaster("local[2]")
      .set("spark.executor.memory", "1g")
      .set("spark.rdd.compress","true")
    val ssc = new StreamingContext(conf, Seconds(1))
//    val drone1 = ssc.sparkContext.broadcast(Map(1 -> 2))
    var drone1Broadcast = ssc.sparkContext.broadcast(Status("drone1","37.422570","-122.176514","1.655","3"))
    var drone2Broadcast = ssc.sparkContext.broadcast(Status("drone2","37.426896017","-122.173091007","1.655","3"))
    val producerPool = ssc.sparkContext.broadcast(KafkaPool(brokers))

//  initialize drone 1 and 2 to random coordinates
//    var drone1 = Status("drone1","37.422570","-122.176514","1.655","3")
//    var drone2 = Status("drone2","37.426896017","-122.173091007","1.655","3")
//    var initFlag = 0;
//    simProducer(conflict, producerPool.value, ssc)
    simProducerLive(conflict, producerPool.value, ssc, drone1Broadcast, drone2Broadcast)
  }

  case class Status(
      flightId: String,
      lat: String,      // in m
      lon: String,      // in m
      speed: String,    // in m/s
      heading: String)  // in rad

  /** Ingests simulator app messages from Kafka to produce conflict messages. */
  def simProducer(
      conflict: String,
      producer: KafkaPool,
      ssc: StreamingContext): Unit = {

    // direct Kafka stream with brokers and topics
    val topicsSet = "status".split(",").toSet
//    println(topicsSet.toString())
    val kafkaParams = Map[String, String]("metadata.broker.list" -> "localhost:9092")

    val statusStream: InputDStream[(String, String)] =
      KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](
        ssc, kafkaParams, topicsSet)

    // map-reduce statuses in <statusStream> into conflict json string; note assumption
    // that every rdd in the dstream contains all relevant aircraft without cutoff

    val statusStrings = statusStream.map { status =>
      println("status" + status)
      implicit val formats = DefaultFormats
      getDroneString(parse(status._2).extract[Status])
    }
//    statusStream.flatMap()
//    val statusStrings = statusStream.flatMap { status =>
//      println("status_2: " + status._2)
//      status._2.split("~")
//    }.map{ raw_status =>
//      println("status_raw: " + raw_status)
//      implicit val formats = DefaultFormats
//      getDroneString(parse(raw_status).extract[Status])
//    }
//

    ssc.checkpoint("ckpt-status")

    val conflicts = statusStrings.reduce(_ + _)
    conflicts.map(producer.send(conflict, _)).print(0)  // need output to run ssc

    ssc.start()
    ssc.awaitTermination()
  }

  /** Ingests Live app messages from Kafka to produce conflict messages. */
  def simProducerLive(
                   conflict: String,
                   producer: KafkaPool,
                   ssc: StreamingContext,
                   drone1Broadcast: org.apache.spark.broadcast.Broadcast[Status],
                   drone2Broadcast: org.apache.spark.broadcast.Broadcast[Status]): Unit = {

    // direct Kafka stream with brokers and topics
    val topicsSet = "status".split(",").toSet
    val kafkaParams = Map[String, String]("metadata.broker.list" -> "localhost:9092")

    val statusStream: InputDStream[(String, String)] =
      KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](
        ssc, kafkaParams, topicsSet)
    // map-reduce statuses in <statusStream> into conflict json string; note assumption
    // that every rdd in the dstream contains all relevant aircraft without cutoff
    val statusStrings = statusStream.flatMap { status =>
      println("status_2: " + status._2)
      status._2.split("~")
    }.map{ raw_status =>
      println("status_raw: " + raw_status)
      implicit val formats = DefaultFormats
      getDroneString(parse(raw_status).extract[Status])
    }

    ssc.checkpoint("ckpt-status")

    val conflicts: DStream[String] = statusStrings.reduce(_ + _)

    // conflict. refers to topic, and not an actual conflict
    conflicts.map(producer.send(conflict, _)).print(0)  // need output to run ssc
//    println(getDroneString(Const.drone1) + "++" + getDroneString(Const.drone2))
//    producer.send(conflict, getDroneString(Const.drone1))
//    producer.send(conflict, getDroneString(Const.drone2))

//    conflicts.print(0)

    ssc.start()
    ssc.awaitTermination()
  }
  /** Formats drone flight state into string. */
  def getDroneString(status: Status): String = {
//    base_lat = 37.422570
//    base_long = -122.176514
    var lat1 = 37.422570.toRadians
    var lon1 = -122.176514.toRadians
    var lat2 = status.lat.toFloat.toRadians
    var lon2 = status.lon.toFloat.toRadians
    var dlon = lon2 - lon1
    var dlat = lat2 - lat1
    var R = 6371000

    var lat  = (lon2-lon1) * math.cos((lat1+lat2)/2.0)
    var lon = (lat2-lat1)

    //this is for live drones
    return status.flightId + "%" + (lat * R).toString + "%" +
      (lon * R).toString + "%" +
      status.heading + "%" +
      status.speed + ","

    //this is for simulator
//    return status.flightId + "%" + status.lat + "%" +
//      status.lon + "%" +
//      status.heading + "%" +
//      status.speed + ","

  }
}
