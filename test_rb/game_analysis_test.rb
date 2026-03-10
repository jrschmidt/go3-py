# Tests for Game Analysis Methods

require './go3.rb'

class GameAnalysisTest < Test::Unit::TestCase
  include TestHelpers
  include TestData


  def test_find_same_color_neighbor_groups_1
    # When the point will be added to a single existing group

    board = BoardSpecs.new
    stones = Stones.new("yes")
    analyzer = GroupAnalyzer.new(stones, board)
    group_points = analyzer.group_points


    stones.set_points :red, [ [3,3], [4,3] ]
    stones.set_points :white, [ [3,1], [2,2], [3,2], [5,1], [6,1], [5,3] ]
    stones.set_points :blue, [ [1,2], [2,3], [5,2], [6,2] ]

    group_points.set_points( {color: :red, id: 0}, [ [3,3], [4,3] ] )
    group_points.set_points( {color: :white, id: 0}, [ [3,1], [2,2], [3,2] ] )
    group_points.set_points( {color: :white, id: 1}, [ [5,1], [6,1] ] )
    group_points.set_points( {color: :white, id: 2}, [ [5,3] ] )
    group_points.set_points( {color: :blue, id: 0}, [ [1,2], [2,3] ] )
    group_points.set_points( {color: :blue, id: 1}, [ [5,2], [6,2] ] )

    ngroups = analyzer.find_prior_same_color_neighbor_groups([6,3],:white)
    assert_equal( ngroups, [ {id: 2, stones: [ [5,3] ]} ] )
  end


  def test_find_same_color_neighbor_groups_2
    # When the point will be added to two groups after they are merged

    board = BoardSpecs.new
    stones = Stones.new("yes")
    analyzer = GroupAnalyzer.new(stones, board)
    group_points = analyzer.group_points


    stones.set_points :red, [ [3,2], [4,2], [4,4], [5,4], [6,3], [7,3] ]
    stones.set_points :white, [ [5,2], [6,2] ]
    stones.set_points :blue, [ [1,2], [2,3], [3,3] ]

    group_points.set_points( {color: :red, id: 0}, [ [3,2], [4,2] ] )
    group_points.set_points( {color: :red, id: 1}, [ [6,3], [7,3] ] )
    group_points.set_points( {color: :red, id: 2}, [ [4,4], [5,4] ] )
    group_points.set_points( {color: :white, id: 0}, [ [5,2], [6,2] ] )
    group_points.set_points( {color: :blue, id: 0}, [ [1,2], [2,3], [3,3] ] )

    expected = [ {id: 1, stones: [ [6,3], [7,3] ] },
                 {id: 2, stones: [ [4,4], [5,4] ] } ]

    ngroups = analyzer.find_prior_same_color_neighbor_groups([6,4],:red)
    assert_contain_same_objects ngroups, expected
  end


  def test_find_other_color_neighbor_groups

    board = BoardSpecs.new
    stones = Stones.new("yes")
    analyzer = GroupAnalyzer.new(stones, board)
    group_points = analyzer.group_points

    stones.set_points :red, [ [3,3], [4,3] ]
    stones.set_points :white, [ [3,1], [2,2], [3,2], [5,1], [6,1], [5,3] ]
    stones.set_points :blue, [ [1,2], [2,3], [5,2], [6,2] ]

    group_points.set_points( {color: :red, id: 0}, [ [3,3], [4,3] ] )
    group_points.set_points( {color: :white, id: 0}, [ [3,1], [2,2], [3,2] ] )
    group_points.set_points( {color: :white, id: 1}, [ [5,1], [6,1] ] )
    group_points.set_points( {color: :white, id: 2}, [ [5,3] ] )
    group_points.set_points( {color: :blue, id: 0}, [ [1,2], [2,3] ] )
    group_points.set_points( {color: :blue, id: 1}, [ [5,2], [6,2] ] )

    ocgroups = analyzer.find_other_color_neighbor_groups([4,2],:white)
    nbr_red = ocgroups.find {|grp| grp[:color] == :red }
    nbr_blue = ocgroups.find {|grp| grp[:color] == :blue }

    assert_not_nil nbr_red
    assert_not_nil nbr_blue

  end


  def test_get_group_stones

    board = BoardSpecs.new
    stones = Stones.new("yes")
    analyzer = GroupAnalyzer.new(stones, board)
    group_points = analyzer.group_points

    stones.set_points :red, [ [2,4], [3,4], [4,5], [4,6], [3,7], [4,7], [5,7] ]
    stones.set_points :white, [ [2,3], [3,3], [3,2], [6,2], [6,5], [7,6] ]
    stones.set_points :blue, [ [3,5], [3,6], [5,3], [6,3], [7,4], [8,5] ]

    group_points.set_points( {color: :red, id: 0}, [ [2,4], [3,4], [4,5], [4,6], [3,7], [4,7], [5,7] ] )
    group_points.set_points( {color: :white, id: 0}, [ [2,3], [3,3], [3,2] ] )
    group_points.set_points( {color: :white, id: 1}, [ [6,2] ] )
    group_points.set_points( {color: :white, id: 2}, [ [6,5], [7,6] ] )
    group_points.set_points( {color: :blue, id: 0}, [ [5,3], [6,3], [7,4], [8,5] ] )
    group_points.set_points( {color: :blue, id: 1}, [ [3,5], [3,6] ] )

    exp_red0 = [ [2,4], [3,4], [4,5], [4,6], [3,7], [4,7], [5,7] ]
    exp_white0 = [ [2,3], [3,3], [3,2] ]
    exp_white1 = [ [6,2] ]
    exp_white2 = [ [6,5], [7,6] ]
    exp_blue0 = [ [5,3], [6,3], [7,4], [8,5] ]
    exp_blue1 = [ [3,5], [3,6] ]

    red0 = analyzer.get_group_stones(:red, 0)
    white0 = analyzer.get_group_stones(:white, 0)
    white1 = analyzer.get_group_stones(:white, 1)
    white2 = analyzer.get_group_stones(:white, 2)
    blue0 = analyzer.get_group_stones(:blue, 0)
    blue1 = analyzer.get_group_stones(:blue, 1)

    assert_contain_same_objects exp_red0, red0
    assert_contain_same_objects exp_white0, white0
    assert_contain_same_objects exp_white1, white1
    assert_contain_same_objects exp_white2, white2
    assert_contain_same_objects exp_blue0, blue0
    assert_contain_same_objects exp_blue1, blue1

  end


  def test_find_all_groups_1

    board = BoardSpecs.new
    stones = Stones.new("yes")
    analyzer = GroupAnalyzer.new(stones, board)

    set_test_groups(stones,1)

    groups = analyzer.find_all_groups()
    assert_rwb_hash(groups, Array)

    red = groups[:red]
    white = groups[:white]
    blue = groups[:blue]

    assert_equal red.size, 1
    assert_equal white.size, 3
    assert_equal blue.size, 3

    red_exp_0 = [ [2, 4], [3, 4], [4, 5], [4, 6], [3, 7], [4, 7], [5, 7] ]
    assert_contain_same_objects red_exp_0, red[0]

    white_exp = [ [ [2, 3], [3, 2], [3, 3] ],
                  [ [7, 4], [8, 5] ],
                  [ [10, 7], [10, 8] ] ]

    white_exp.each do |xgrp|
      assert_not_nil white.find {|group| contain_same_objects(xgrp,group) }
    end

    blue_exp = [ [ [5, 3] ],
                 [ [3, 5], [3, 6] ],
                 [ [7, 8], [8, 8], [7, 9], [9, 9] ] ]

    blue_exp.each do |xgrp|
      assert_not_nil blue.find {|group| contain_same_objects(xgrp,group) }
    end

  end


  def test_find_all_groups_3

    board = BoardSpecs.new
    stones = Stones.new("yes")
    analyzer = GroupAnalyzer.new(stones, board)

    set_test_groups(stones,3)

    groups = analyzer.find_all_groups()
    assert_rwb_hash(groups, Array)

    red = groups[:red]
    white = groups[:white]
    blue = groups[:blue]

    assert_equal red.size, 3
    assert_equal white.size, 4
    assert_equal blue.size, 7

    red_exp = [ [ [3,7], [4,7], [5,7] ],
                [ [2,4], [2,3], [1,2] ],
                [ [3,1], [3,2], [4,3], [5,3], [5,2] ] ]

    red_exp.each do |xgrp|
      assert_not_nil red.find {|group| contain_same_objects(xgrp,group) }
    end

    white_exp = [ [ [3,4], [4,5], [5,5], [5,4], [6,4], [7,4], [8,4] ],
                  [ [1,6], [2,6], [2,5] ],
                  [ [6,1], [7,2], [6,2] ],
                  [ [6,7], [7,7], [8,7] ] ]

    white_exp.each do |xgrp|
      assert_not_nil white.find {|group| contain_same_objects(xgrp,group) }
    end

    blue_exp = [ [ [1,1], [2,1] ],
                 [ [4,1], [4,2] ],
                 [ [3,3], [4,4] ],
                 [ [6,3], [7,3], [8,3] ],
                 [ [1,4], [1,5] ],
                 [ [3,5], [3,6], [4,6] ],
                 [ [6,6], [6,5], [7,5], [8,6] ] ]

    blue_exp.each do |xgrp|
      assert_not_nil blue.find {|group| contain_same_objects(xgrp,group) }
    end

  end


  def test_find_group_airpoints

    board = BoardSpecs.new
    stones = Stones.new("yes")
    analyzer = GroupAnalyzer.new(stones, board)

    set_test_groups(stones,1)

    # Red Group #1 - 7 stones, 13 airpoints
    red1 = { stones: [ [3,4], [4,6], [4,7], [4,5], [2,4], [3,7], [5,7] ],
             expected_points: [ [4,4], [5,5], [5,6], [6,7], [6,8], [5,8], [4,8], [3,8], [2,7], [2,6], [2,5], [1,4], [1,3] ] }

    # White Group #1 - 2 stones, 8 airpoints
    white1 = { stones: [ [7,4], [8,5] ],
               expected_points: [ [6,3], [7,3], [8,4], [9,5], [9,6], [8,6], [7,5], [6,4] ] }

    # White Group #2 - 3 stones, 8 airpoints
    white2 = { stones: [ [3,3], [2,3], [3,2] ] ,
               expected_points: [ [1,3], [1,2], [2,2], [2,1], [3,1], [4,2], [4,3], [4,4] ] }

    # White Group #3 - 2 stones, 8 airpoints
    white3 = { stones: [ [10,8], [10,7] ] ,
             expected_points: [ [9,6], [10,6], [11,7], [11,8], [11,9], [10,9], [9,8], [9,7] ] }

    # Blue Group #1 - 1 stone, 6 airpoints
    blue1 = { stones: [ [5,3] ] ,
             expected_points: [ [5,2], [6,3], [6,4], [5,4], [4,3], [4,2] ] }

    # Blue Group #2 - 2 stones, 2 airpoints
    blue2 = { stones: [ [3,5], [3,6] ] ,
             expected_points: [ [2,5], [2,6] ] }

    # Blue Group #3 - 4 stones, 12 airpoints
    blue3 = { stones: [ [7,8], [9,9], [7,9], [8,8] ] ,
             expected_points: [ [6,7], [7,7], [8,7], [9,8], [10,9], [10,10], [9,10], [8,9], [8,10], [7,10], [6,9], [6,8] ] }

    groups = [red1, white1, white2, white3, blue1, blue2, blue3]

    for group in groups
      spaces = analyzer.find_group_airpoints(group[:stones])
      assert_contain_same_objects group[:expected_points], spaces
    end
  end


  def test_find_empty_points_for_groups

    board = BoardSpecs.new
    stones = Stones.new("yes")
    analyzer = GroupAnalyzer.new(stones, board)

    set_test_groups(stones,3)
    groups = analyzer.find_all_groups

    empty_points = analyzer.find_empty_points_for_groups(groups)

    red = empty_points.find_all {|group| group[:color] == :red }
    white = empty_points.find_all {|group| group[:color] == :white }
    blue = empty_points.find_all {|group| group[:color] == :blue }

    assert_equal red.size, 3
    assert_equal white.size, 4
    assert_equal blue.size, 7

    red_exp = [ {eyes: [[1,3], [2,2]],
                 points: [[1,2], [2,3], [2,4]] },

                {eyes: [[2,2], [5,1]],
                 points: [[3,1], [3,2], [4,3], [5,3], [5,2]] },

                {eyes: [[2,7], [3,8], [4,8], [5,8], [6,8], [5,6]],
                 points: [[3,7], [4,7], [5,7]] } ]

    red_exp.each do |xgrp|
      # FIXME Can this be replaced with includes?, or something similar, called on the Hash object?
      assert_not_nil red.find {|group| contain_same_objects(xgrp[:eyes], group[:eyes]) }
      assert_not_nil red.find {|group| contain_same_objects(xgrp[:points], group[:points]) }
    end

    white_exp = [ {eyes: [[5,1]],
                   points: [[6,1], [6,2], [7,2]] },

                  {eyes: [[2,7]],
                   points: [[1,6], [2,6], [2,5]] },

                  {eyes: [[5,6], [8,5], [9,5], [9,4]],
                   points: [[3,4], [4,5], [5,5], [5,4], [6,4], [7,4], [8,4]] },

                  {eyes: [[6,8], [7,8], [8,8], [9,8], [9,7], [5,6], [7,6]],
                   points: [[6,7], [7,7], [8,7]] } ]

    white_exp.each do |xgrp|
      assert_not_nil white.find {|group| contain_same_objects(xgrp[:eyes], group[:eyes]) }
      assert_not_nil white.find {|group| contain_same_objects(xgrp[:points], group[:points]) }
    end

    blue_exp = [ {eyes: [[2,2]],
                  points: [[1,1], [2,1]] },

                 {eyes: [[2,2]],
                  points: [[3,3], [4,4]] },

                 {eyes: [[5,1]],
                  points: [[4,1], [4,2]] },

                 {eyes: [[1,3]],
                  points: [[1,4], [1,5]] },

                 {eyes: [[5,6]],
                  points: [[3,5], [3,6], [4,6]] },

                 {eyes: [[9,4]],
                  points: [[6,3], [7,3], [8,3]] },

                 {eyes: [[5,6], [7,6], [8,5], [9,6], [9,7]],
                  points: [[6,6], [6,5], [7,5], [8,6]] } ]

    blue_exp.each do |xgrp|
      assert_not_nil blue.find {|group| contain_same_objects(xgrp[:eyes], group[:eyes]) }
      assert_not_nil blue.find {|group| contain_same_objects(xgrp[:points], group[:points]) }
    end

  end


  def test_find_dead_groups

    board = BoardSpecs.new
    stones = Stones.new("yes")
    analyzer = GroupAnalyzer.new(stones, board)

    stones.set_point([3,4], :red)
    assert_equal analyzer.dead_groups?(:white), []
    assert_equal analyzer.dead_groups?(:blue), []

    stones.set_point([4,5], :white)
    assert_equal analyzer.dead_groups?(:red), []
    assert_equal analyzer.dead_groups?(:blue), []

    stones.set_point([5,6], :blue)
    assert_equal analyzer.dead_groups?(:red), []
    assert_equal analyzer.dead_groups?(:white), []

    stones.set_point([5,5], :red)
    assert_equal analyzer.dead_groups?(:white), []
    assert_equal analyzer.dead_groups?(:blue), []

    stones.set_point([11,8], :white)
    assert_equal analyzer.dead_groups?(:red), []
    assert_equal analyzer.dead_groups?(:blue), []

    stones.set_point([4,6], :blue)
    assert_equal analyzer.dead_groups?(:red), []
    assert_equal analyzer.dead_groups?(:white), []

    stones.set_point([4,4], :red)
    assert_equal analyzer.dead_groups?(:white), []
    assert_equal analyzer.dead_groups?(:blue), []

    stones.set_point([11,9], :white)
    assert_equal analyzer.dead_groups?(:red), []
    assert_equal analyzer.dead_groups?(:blue), []

    # BLUE PLAY AT [3,5] KILLS WHITE STONE AT [4,5]
    stones.set_point([3,5], :blue)
    assert_equal analyzer.dead_groups?(:red), []
    wh = analyzer.dead_groups?(:white)
    assert wh.include? [ [4,5] ]

    stones.set_point([10,7], :red)
    # List of dead white groups will be unchanged
    assert_equal analyzer.dead_groups?(:white), wh
    assert_equal analyzer.dead_groups?(:blue), []

    stones.set_point([5,8], :white)
    assert_equal analyzer.dead_groups?(:red), []
    assert_equal analyzer.dead_groups?(:blue), []

    stones.set_point([10,9], :blue)
    assert_equal analyzer.dead_groups?(:red), []
    assert_equal analyzer.dead_groups?(:white), wh

    stones.set_point([10,8], :red)
    assert_equal analyzer.dead_groups?(:white), wh
    assert_equal analyzer.dead_groups?(:blue), []

    stones.set_point([7,10], :white)
    assert_equal analyzer.dead_groups?(:red), []
    assert_equal analyzer.dead_groups?(:blue), []

    stones.set_point([11,10], :blue)
    assert_equal analyzer.dead_groups?(:red), []
    assert_equal analyzer.dead_groups?(:white), wh

    # RED PLAY AT [11,7] KILLS WHITE STONES AT [11,8] and [11,9]
    stones.set_point([11,7], :red)
    assert_equal analyzer.dead_groups?(:blue), []
    wh = analyzer.dead_groups?(:white)
    assert (wh.include? [ [11,8], [11,9] ] ) || (wh.include? [ [11,9], [11,8] ] )

  end


  def test_make_move_remove_dead_groups

    processor = MoveProcessor.new
    stones = Stones.new("yes")
    processor.stones = stones
    board = BoardSpecs.new
    analyzer = GroupAnalyzer.new(stones, board)
    processor.analyzer = analyzer

    processor.make_move(:red, [3,4])
    processor.make_move(:white, [4,5])
    processor.make_move(:blue, [5,6])
    processor.make_move(:red, [5,5])
    processor.make_move(:white, [11,8])
    processor.make_move(:blue, [4,6])
    processor.make_move(:red, [4,4])
    processor.make_move(:white, [11,9])

    # BLUE PLAY AT [3,5] KILLS WHITE STONE AT [4,5]
    # We don't find the dead white group because it's already been removed by
    # the remove_dead_stones_after_move method, which was called by make_move.
    processor.make_move(:blue, [3,5])
    assert_equal stones.get_point([4,5]), :empty
    assert_equal analyzer.dead_groups?(:red), []
    assert_equal analyzer.dead_groups?(:white), []

    processor.make_move(:red, [10,7])
    processor.make_move(:white, [5,8])
    processor.make_move(:blue, [10,9])
    processor.make_move(:red, [10,8])
    processor.make_move(:white, [7,10])
    processor.make_move(:blue, [11,10])

    # RED PLAY AT [11,7] KILLS WHITE STONES AT [11,8] and [11,9]
    # We don't find the dead white group because it's already been removed by
    # the remove_dead_stones_after_move method, which was called by make_move.
    processor.make_move(:red, [11,7])
    assert_equal stones.get_point([11,8]), :empty
    assert_equal stones.get_point([11,9]), :empty
    assert_equal analyzer.dead_groups?(:white), []
    assert_equal analyzer.dead_groups?(:blue), []

  end


  def test_find_one_eye_points

    board = BoardSpecs.new
    stones = Stones.new("yes")
    analyzer = GroupAnalyzer.new(stones, board)

    set_test_groups(stones,3)

    eyes = analyzer.find_one_eye_points
    assert_equal eyes.class, Array
    assert eyes.include? [2,2]
    assert eyes.include? [1,3]
    assert eyes.include? [5,1]
    assert eyes.include? [5,6]
    assert eyes.include? [7,6]
    refute eyes.include? [9,4]
    refute eyes.include? [4,4]
    refute eyes.include? [10,9]
    refute eyes.include? [8,10]

  end



end
