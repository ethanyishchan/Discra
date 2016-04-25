package ingestor

import ingestor.Ingestor.Status

object Const {
  final val MessagePeriod = 5000  // milliseconds

  final val NConflict = 10
  final val MaxID = 100000
  final val MaxDrones = 3

  final val MinX = -120.0
  final val MaxX = 120.0

  final val MinY = -120.0
  final val MaxY = 120.0

  final val MinHeading = 0.0
  final val MaxHeading = 6.28319

  final val MinSpeed = 3.0
  final val MaxSpeed = 7.0

  var drone1 = Status("drone1","37.422570","-122.176514","1.655","3")
  var drone2 = Status("drone2","37.426896017","-122.173091007","1.655","3")
  //  final val MessagePeriod = 5000  // milliseconds
//
//  final val NConflict = 10
//  final val MaxID = 100000
//  final val MaxDrones = 3
//
//  final val MinX = -2000.0
//  final val MaxX = 2000.0
//
//  final val MinY = -2000.0
//  final val MaxY = 2000.0
//
//  final val MinHeading = 0.0
//  final val MaxHeading = 6.28319
//
//  final val MinSpeed = 10.0
//  final val MaxSpeed = 20.0
}
