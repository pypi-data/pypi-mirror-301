import random

import networkx as nx


def install(eng, seed=None):
	if seed is not None:
		random.seed(seed)
	grid: nx.Graph = nx.grid_2d_graph(100, 100)

	for node in list(grid):
		if random.random() < 0.1:
			grid.remove_node(node)
		elif random.random() < 0.005:
			grid.add_node(f"{node}_inhabitant", location=node)

	phys = eng.new_character("physical", grid)

	@eng.function
	def find_path_somewhere(node):
		from logging import getLogger
		from networkx.algorithms import astar_path
		from math import sqrt

		logger = getLogger("pathfind")

		x, y = node.location.name
		destx = 100 - int(x)
		desty = 100 - int(y)
		while (destx, desty) not in node.character.place:
			if destx < 99:
				destx += 1
			elif desty < 99:
				destx = 0
				desty += 1
			else:
				destx = desty = 0
		ret = astar_path(
			node.character,
			node.location.name,
			(destx, desty),
			lambda a, b: sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2),
		)
		logger.debug(f"{node.name}'s shortest path to {destx, desty} is {ret}")
		return ret

	@phys.rule
	def go_places(char):
		from networkx.exception import NetworkXNoPath

		def log_as_completed(fut):
			try:
				char.engine.debug(
					f"Got path for {fut.thing.name}: {fut.result()}"
				)
			except NetworkXNoPath:
				char.engine.debug(f"No path for {fut.thing.name}")

		futs = []
		with char.engine.pool as pool:
			for thing in char.thing.values():
				fut = pool.submit(
					char.engine.function.find_path_somewhere, thing
				)
				fut.thing = thing
				fut.add_done_callback(log_as_completed)
				futs.append(fut)
		with char.engine.batch():
			for fut in futs:
				try:
					result = fut.result()
					thing = fut.thing
					thing.follow_path(result, check=False)
					char.engine.debug(f"followed path for thing {thing.name}")
				except NetworkXNoPath:
					char.engine.debug(
						f"got no path for thing {fut.thing.name}"
					)
					continue

	@go_places.trigger
	def turn_one_only(char):
		return char.engine.turn == 1
