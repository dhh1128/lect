class job:
  func get_node_range:
    takes:
      req: requirement +const
      node: node +const
      required_range: rsv_range
      requested_range_count: int +range(1)
    returns:
      error: int = 0 # by init'ing here, we're specifying what to return unless overridden
      affinity: str = null
      resv_type: rsv_type_enum
      avail_range: rsv_range[]
      dedicated_res: resource[]
      seek_long: bool
      blocking_res: str
    impl:
      # If node is down, and system's not going to revalidate any
      # time soon, then exit early with failure.
      if job.unlimited down state delay time specified and node is in down/bad state:
        return