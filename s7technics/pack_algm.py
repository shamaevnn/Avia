from rectpack import newPacker

packer = newPacker()

airplanes = {
	'Ил-96-300': (round(55.345), round(57.66)),
	'Ил-96-400': (round(63.939), round(60.105)),
	'Ту-154М': (round(47.9), round(37.55)),
	'Ан-24': (round(23.53), round(29.2)),
	'Ан-124': (round(69.1), round(73.3)),
	'A319': (round(33.84), round(34.1)),
	'A320': (round(37.57), round(34.1)),
	'A321': (round(44.51), round(34.1)),
	'737-200': (round(30.53), round(28.35)),
	'737-300': (round(33.25), round(28.88)),
	'737-800': (round(39.47), round(34.32)),
}

airports = {
	'DME': (300, 80),
	'SVO': (200, 90),
	'VKO': (150, 70),
}


# Add the rectangles to packing queue
for r in airplanes.values():
	packer.add_rect(*r)

# Add the bins where the rectangles will be placed
for b in airports.values():
	packer.add_bin(*b)

# Start packing
packer.add_bin(*airports['DME'])
packer.pack()
