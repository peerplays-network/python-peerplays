from peerplaysbase.transactions import formatTimeFromNow
from pprint import pprint
from grapheneapi.grapheneapi import GrapheneAPI
rpc = GrapheneAPI("localhost", 8092)

op = rpc.get_prototype_operation("betting_market_rules_create_operation")

op[1]["name"] = [["en", "NHL Rules v1.0"]]
op[1]["description"] = [["en", "The winner will be the team with the most points at the end of the game.  The team with fewer points will not be the winner."]]

handle = rpc.begin_builder_transaction()
rpc.add_operation_to_builder_transaction(handle, op)
rpc.set_fees_on_builder_transaction(handle, "1.3.0")
pprint(rpc.propose_builder_transaction2(handle, "init0", formatTimeFromNow(60), 0, True))
