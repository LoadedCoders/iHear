package edu.umkc.helpers

import java.io.{DataInputStream, IOException, PrintStream}
import java.net.{InetAddress, Socket}

import edu.umkc.ihear.iHApp

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
    println("Sending .. : "+ string)
    try {
      lazy val address: Array[Byte] = Array(192.toByte, 168.toByte, 0.toByte, 15.toByte)
      val ip = InetAddress.getByAddress(address)
//      val ip = InetAddress.getByName(iHApp.iOS_IP).getHostName
      val socket = new Socket(ip, 1234)
      val out = new PrintStream(socket.getOutputStream)
//      val in = new DataInputStream(socket.getInputStream)

      out.print(string)
      out.flush()

      out.close()
//      in.close()
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
