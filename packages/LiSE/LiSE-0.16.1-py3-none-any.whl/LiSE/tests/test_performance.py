from time import monotonic

import networkx as nx

from LiSE import Engine


def test_follow_path(tmp_path):
	big_grid = nx.grid_2d_graph(100, 100)
	big_grid.add_node("them", location=(0, 0))
	straightly = nx.shortest_path(big_grid, (0, 0), (99, 99))
	with Engine(tmp_path) as eng:
		grid = eng.new_character("grid", big_grid)
		them = grid.thing["them"]
		start = monotonic()
		them.follow_path(straightly)
		elapsed = monotonic() - start
		assert (
			elapsed < 1.0
		), f"Took too long to follow a path of length {len(straightly)}: {elapsed:.2} seconds"
