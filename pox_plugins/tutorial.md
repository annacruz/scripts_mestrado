##Follow the instructions to run this pox plugin correctly


- On a Terminal

    ssh -X <machine>
    sudo mn --topo single,3 --mac --switch ovsk --controller remote
    xterm h1 h2

- On h1 opened terminal

    iperf -c <ip_h2> -p <port> -t <time_in_seconds>

- On h2 opened terminal
    iperf -p <port> -s

- On Another Terminal

    ssh <machine>
    ./pox.py forwarding.l2_learning flow_stats_mod


Obs: This is the tutorial if mininet and pox controller are in the same machine.
