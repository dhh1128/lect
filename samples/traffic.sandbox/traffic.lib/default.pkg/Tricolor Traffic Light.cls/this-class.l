Tricolor Traffic Light: class
	extends: Sign
	implements: GPS Point of Interest, City Infrastructure
	properties:
		- location
    - current color: Traffic Light Color +null
		- next color change: Date +null
		- # How long the light is red or green
		- wait time: units(seconds) = 45 +range[10..90]
		# How long the light is yellow
		- transition time: units(seconds) = 15 +range[2..wait time / 2]
		# How long both directions are red
		- overlap time: units(seconds) = max(wait time / 3, 8) +range[1..10]
		- power enabled: bool = false
