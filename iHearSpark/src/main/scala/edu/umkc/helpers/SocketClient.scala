package edu.umkc.helpers

import java.io.{DataInputStream, IOException, PrintStream}
import java.net.{InetAddress, Socket}

/**
 * Created by Mayanka on 10-Sep-15.
 */
object SocketClient {

  val socket: Option[Socket] = None

  def findIpAdd(): String = {
    val localhost = InetAddress.getLocalHost
    val localIpAddress = localhost.getHostAddress

    localIpAddress
  }



  def sendCommandToRobot(string: String) {
    // Simple server

    try {
      lazy val address: Array[Byte] = Array(10.toByte, 205.toByte, 0.toByte, 5.toByte)
      val ia = InetAddress.getByAddress(address)
      val socket = new Socket(ia, 1234)
      val out = new PrintStream(socket.getOutputStream)
      val in = new DataInputStream(socket.getInputStream)

      out.print(string)
      out.flush()

      out.close()
      in.close()
      socket.close()
    }
    catch {
      case e: IOException =>
        e.printStackTrace()
    }
  }

  def main(args: Array[String]) {

  }
}
