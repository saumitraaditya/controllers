import uuid
import time
import random
from controller.modules.Topology import DiscoveredPeer
from controller.modules.GraphBuilder import GraphBuilder


def main():
    max_nodes = 20
    node_ids = [None] * max_nodes
    DiscoveredPeer.ExclusionBaseInterval = 3
    known_peers = {}
    xcl_cnt = 6
    excl_pid = [None] * xcl_cnt
    max_rmv_time = 1

    for i in range(0, max_nodes):
        peer_id = str(uuid.uuid4().hex)[:7]
        node_ids[i] = peer_id
        known_peers[peer_id] = DiscoveredPeer(peer_id)
    print("TEST 1")
    print("Known peers all enabled\n{0}".format(known_peers))
    for i in range(0, xcl_cnt):
        idx = random.randint(0, max_nodes)
        excl_pid[i] = node_ids[idx]
        print("Excluded {0}th node {1}".format(idx, excl_pid[i]))
        known_peers[excl_pid[i]].exclude()
        if known_peers[excl_pid[i]].removal_time > max_rmv_time:
            max_rmv_time = known_peers[excl_pid[i]].removal_time

    peer_list = [peer_id for peer_id in known_peers \
                if not known_peers[peer_id].is_excluded]
    print("Avialable peers list ={0}\n{1}".format(len(peer_list), peer_list))
    print("Discovered peers \n{0}".format(known_peers))


    sleep_time = max_rmv_time - time.time()
    print("Waiting {0} secs until exclusion expired".format(sleep_time))
    while time.time() < max_rmv_time:
        time.sleep(5)
        peer_list = [peer_id for peer_id in known_peers \
                    if not known_peers[peer_id].is_excluded]
        print("Recovering peers={0}\n{1}".format(len(peer_list), peer_list))

    print("Discovered peers \n{0}".format(known_peers))
    print("TEST 2")
    xcl_cnt = 12
    excl_pid = [None] * xcl_cnt
    for i in range(0, xcl_cnt):
        idx = random.randint(0, max_nodes)
        excl_pid[i] = node_ids[idx]
        print("Excluded {0}th node {1}".format(idx, excl_pid[i]))
        known_peers[excl_pid[i]].exclude()
        if known_peers[excl_pid[i]].removal_time > max_rmv_time:
            max_rmv_time = known_peers[excl_pid[i]].removal_time

    peer_list = [peer_id for peer_id in known_peers \
                if not known_peers[peer_id].is_excluded]
    print("Avialable peers list ={0}\n{1}".format(len(peer_list), peer_list))
    print("Discovered peers \n{0}".format(known_peers))

    for peer_id in excl_pid:
        known_peers[peer_id].restore()
    print("Discovered peers \n{0}".format(known_peers))

if __name__ == "__main__":
    main()

        #    self.logger.info('datapath         port     '
    #                     'rx-pkts  rx-bytes rx-error '
    #                     'tx-pkts  tx-bytes tx-error')
    #    self.logger.info('---------------- -------- '
    #                     '-------- -------- -------- '
    #                     '-------- -------- --------')
    #    for stat in sorted(body, key=attrgetter('port_no')):
    #        self.logger.info('%016x %8x %8d %8d %8d %8d %8d %8d',
    #                         ev.msg.datapath.id, stat.port_no,
    #                         stat.rx_packets, stat.rx_bytes, stat.rx_errors,
    #                         stat.tx_packets, stat.tx_bytes, stat.tx_errors)
