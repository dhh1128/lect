enable power: func +public
  takes:
    - new state: bool
	code: |
		if new state != power enabled:
			if new state:
				this.current color = Traffic Light Color.red
				this.start countdown()
			else:
				this.interrupt countdown()
				this.current color = null
				this.next color change = null

