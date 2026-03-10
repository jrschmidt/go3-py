  # Test Data Setting Methods

module TestData

  def set_test_groups(point_set, index)

    case index
    when 1
      point_set.set_points :red, [ [3,4], [4,6], [4,7], [4,5], [2,4], [3,7], [5,7] ]
      point_set.set_points :white, [ [7,4], [8,5], [3,3], [2,3], [3,2], [10,8], [10,7] ]
      point_set.set_points :blue, [ [5,3], [3,5], [3,6], [7,8], [9,9], [7,9], [8,8] ]

    when 2
      point_set.set_points :red, [ [6,1], [4,3], [6,3], [2,4], [4,4], [6,4], [3,5], [6,5] ]
      point_set.set_points :white, [ [1,1], [2,2], [3,2], [4,2], [5,2], [4,5], [4,6], [5,6] ]
      point_set.set_points :blue, [ [2,1], [3,1], [4,1], [6,2], [7,2], [3,3], [5,3], [3,4], [5,4] ]

    when 3
      point_set.set_points :red, [ [3,1], [1,2], [3,2], [5,2], [2,3], [4,3], [5,3], [2,4], [3,7], [4,7], [5,7] ]
      point_set.set_points :white, [ [6,1], [6,2], [7,2], [3,4], [5,4], [6,4], [7,4], [8,4], [2,5], [4,5], [5,5], [1,6], [2,6], [6,7], [7,7], [8,7] ]
      point_set.set_points :blue, [ [1,1], [2,1], [4,1], [4,2], [3,3], [6,3], [7,3], [8,3], [1,4], [4,4], [1,5], [3,5], [6,5], [7,5], [3,6], [4,6], [6,6], [8,6] ]
    end
  end


end
