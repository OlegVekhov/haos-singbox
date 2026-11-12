package main

import (
 "bytes"
 "encoding/binary"
 "io"
 "net"
 "testing"
 "time"
)

func TestAddress(t *testing.T) {
 for _, input := range [][]byte{
  {1, 5, 253, 63, 222, 0, 53},
  {4, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,53},
  {3,3,'a','b','c',0,53},
 } {
  got, err := addr(bytes.NewReader(input))
  if err != nil || !bytes.Equal(input,got) { t.Fatalf("addr %x: %x, %v",input,got,err) }
 }
}

func TestRelayAddress(t *testing.T) {
 a,err:=parseRelay([]byte{1,0,0,0,0,0,53})
 if err!=nil || a.Port!=53 || !a.IP.Equal(net.ParseIP("127.0.0.1")) { t.Fatal(a,err) }
}

func TestHevFrameAndUDP(t *testing.T) {
 udp,err:=net.ListenUDP("udp",&net.UDPAddr{IP:net.ParseIP("127.0.0.1")})
 if err!=nil { t.Fatal(err) }; defer udp.Close()
 go func(){b:=make([]byte,65535);for{n,a,e:=udp.ReadFromUDP(b);if e!=nil{return};udp.WriteToUDP(b[:n],a)}}()
 upstream,err:=net.Listen("tcp","127.0.0.1:0");if err!=nil{t.Fatal(err)};defer upstream.Close()
 go func(){c,e:=upstream.Accept();if e!=nil{return};defer c.Close();read(c,3);c.Write([]byte{5,0});read(c,3);addr(c);p:=uint16(udp.LocalAddr().(*net.UDPAddr).Port);c.Write([]byte{5,0,0,1,127,0,0,1,byte(p>>8),byte(p)});io.Copy(io.Discard,c)}()
 client,server:=net.Pipe();defer client.Close()
 done:=make(chan error,1);go func(){done<-serve(server,upstream.Addr().String(),"","")}()
 client.Write([]byte{5,1,0});reply,_:=read(client,2);if !bytes.Equal(reply,[]byte{5,0}) {t.Fatal(reply)}
 client.Write([]byte{5,5,0,1,0,0,0,0,0,0});reply,_=read(client,10);if reply[1]!=0{t.Fatal(reply)}
 dest:=[]byte{1,5,253,63,222,0x14,0xE9}
 payload:=[]byte("wireguard-test")
 b:=[]byte{0,byte(len(payload)),byte(len(dest)+3)}
 b=append(b,dest...);b=append(b,payload...)
 client.Write(b);client.SetReadDeadline(time.Now().Add(time.Second))
 hdr,err:=read(client,3);if err!=nil{t.Fatal(err)}
 if int(binary.BigEndian.Uint16(hdr[:2]))!=len(payload){t.Fatal(hdr)}
 body,err:=read(client,int(hdr[2])-3+len(payload));if err!=nil{t.Fatal(err)}
 if !bytes.Equal(body[len(dest):],payload){t.Fatalf("mismatched UDP reply %x",body)}
 client.Close();select{case <-done:case <-time.After(time.Second):t.Fatal("SOCKS session leaked")}
}
