package main

import (
	"math/rand/v2"
	"net"

	"github.com/google/uuid"
)

type NetworkPlayer struct {
	id   uuid.UUID
	addr net.UDPAddr
}

func NewNetworkPlayer(addr net.UDPAddr) *NetworkPlayer {
	return &NetworkPlayer{
		id:   uuid.New(),
		addr: addr,
	}
}

type Coords struct {
	X float32
	Y float32
}

func NewCoords() *Coords {
	return &Coords{
		X: float32(rand.IntN(1260) + 20),
		Y: float32(rand.IntN(700) + 20),
	}
}

type Color struct {
	r uint8
	g uint8
	b uint8
}

func NewColor() *Color {
	return &Color{
		r: uint8(rand.IntN(256)),
		g: uint8(rand.IntN(256)),
		b: uint8(rand.IntN(256)),
	}
}

type Player struct {
	network NetworkPlayer
	coords  Coords
	size    uint8
	color   Color
}

func NewPlayer(addr net.UDPAddr) *Player {
	return &Player{
		network: *NewNetworkPlayer(addr),
		coords:  *NewCoords(),
		size:    20,
		color:   *NewColor(),
	}
}
