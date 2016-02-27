#!/bin/bash
# Credit: https://gist.github.com/keturn/541339 (@keturn)
#
# Add latency to all outgoing traffic on $DEV on tcp/udp $PORT,
# in the amount of $DELAY.
#
# This is matching on both source port and destination port, which
# may hit you twice if you're accessing a local resource.
#
# To see what's currently in effect,
#   tc -s qdisc show dev lo
#   tc -p filter show dev lo
#
# The quickest way to undo this is to delete all qdiscs on loopback:
#   tc qdisc del dev lo root
#
# This is adding latency, which will make interactivity clunky, but
# it's *not* a cap on throughput, so it doesn't emulate a slow link in
# that respect.
#
# The best reference for this stuff is
# http://tcn.hypert.net/tcmanual.pdf

DEV=lo
PORT=11818
DELAY=150ms

# Create a priority-based queue.
tc qdisc add dev $DEV root handle 1: prio
# Delay everything in band 3
tc qdisc add dev $DEV parent 1:3 handle 30: netem \
     delay $DELAY

# say traffic to $PORT is band 3
tc filter add dev $DEV parent 1:0 \
    protocol ip \
    u32 match ip dport $PORT 0xffff \
    flowid 1:3
tc filter add dev $DEV parent 1:0 \
    protocol ip \
    u32 match ip sport $PORT 0xffff \
    flowid 1:3