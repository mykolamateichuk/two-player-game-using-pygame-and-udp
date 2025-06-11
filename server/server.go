package main

import (
	"fmt"
	"log"
	"net"
	"strconv"
	"strings"
)

const FoodSize = 10

var Players = make(map[string]Player)
var PlayerAddrs = make(map[string]net.UDPAddr)

var CurrentFoodCoords Coords
var ExitCount uint8 = 0

func getOtherPlayer(player Player) Player {
	for _, pl := range Players {
		if pl.network.id != player.network.id {
			return pl
		}
	}
	return player
}

func stringifyCoords(coords Coords) string {
	return fmt.Sprintf("%.2f %.2f", coords.X, coords.Y)
}

func stringifyColor(color Color) string {
	return fmt.Sprintf("%d %d %d", color.r, color.g, color.b)
}

func stringifyPlayerInfo(player Player) string {
	strCoords := stringifyCoords(player.coords)
	strColor := stringifyColor(player.color)

	return fmt.Sprintf("%s %d %s", strCoords, player.size, strColor)
}

func sendToClient(message string, clientAddr net.UDPAddr, ln net.UDPConn) {
	_, err := ln.WriteToUDP([]byte(message), &clientAddr)
	if err != nil {
		log.Fatalf("Error while sending message to client: %s", err)
	}
	log.Printf("Sent %d bytes to %s\n", len(message), clientAddr.String())
}

func handleCollision(player Player) bool {
	if player.coords.X-float32(player.size)-float32(FoodSize) <= CurrentFoodCoords.X &&
		CurrentFoodCoords.X <= player.coords.X+float32(player.size)+float32(FoodSize) {

		if player.coords.Y-float32(player.size)-float32(FoodSize) <= CurrentFoodCoords.Y &&
			CurrentFoodCoords.Y <= player.coords.Y+float32(player.size)+float32(FoodSize) {
			return true
		}
	}
	return false
}

func handleRequest(ln net.UDPConn, addr net.UDPAddr, buf []byte) {
	command := strings.Fields(string(buf))[0]
	args := strings.Fields(string(buf))[1:]

	switch command {
	case "CONN":
		player := *NewPlayer(addr)
		Players[addr.String()] = player
		PlayerAddrs[addr.String()] = addr

		sendToClient(stringifyPlayerInfo(player), addr, ln)

		if len(Players) == 2 {
			sendToClient(stringifyPlayerInfo(getOtherPlayer(player)), addr, ln)
			sendToClient(stringifyPlayerInfo(player), getOtherPlayer(player).network.addr, ln)

			CurrentFoodCoords = *NewCoords()

			for addr := range Players {
				sendToClient(stringifyCoords(CurrentFoodCoords), PlayerAddrs[addr], ln)
			}
		}

	case "COORDS":
		player := Players[addr.String()]

		x, err := strconv.ParseFloat(args[0], 32)
		if err != nil {
			log.Printf("Couldn't parse player's coordinates: %s", err)
		}

		y, err := strconv.ParseFloat(args[1], 32)
		if err != nil {
			log.Printf("Couldn't parse player's coordinates: %s", err)
		}

		player.coords.X = float32(x)
		player.coords.Y = float32(y)
		Players[addr.String()] = player

		if handleCollision(player) {
			player.size += 5
			Players[addr.String()] = player

			CurrentFoodCoords = *NewCoords()
		}

		sendToClient(stringifyCoords(CurrentFoodCoords), addr, ln)
		sendToClient(stringifyPlayerInfo(player), addr, ln)
		sendToClient(stringifyPlayerInfo(getOtherPlayer(player)), addr, ln)

	case "EXIT":
		ExitCount += 1
	}
}

func main() {
	addr, err := net.ResolveUDPAddr("udp", ":8080")
	if err != nil {
		log.Fatalf("Error while resolving the UDP address: %s", err)
	}

	ln, err := net.ListenUDP("udp", addr)
	if err != nil {
		log.Fatalf("Error while setting up listener on %s: %s", addr, err)
	}
	defer ln.Close()

	log.Println("Listening on port 8080...")

	buf := make([]byte, 64)
	for ExitCount != 2 {
		n, addr, err := ln.ReadFromUDP(buf)
		if err != nil {
			log.Fatalf("Error while receiving the request: %s", err)
		}
		log.Printf("Received %d bytes from %s\n", n, addr)

		handleRequest(*ln, *addr, buf[:n])
	}
}
