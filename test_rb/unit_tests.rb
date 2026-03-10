require './go3.rb'

require 'test/unit'


require './test_helpers.rb'
require './test_data.rb'


# Tests for Board Point and Stone Methods
require './board_point_stone_test.rb'

# Tests for Game Analysis Methods
require './game_analysis_test.rb'

# Tests for Legal Moves Methods
require './legal_moves_test.rb'


class Go3Test < Test::Unit::TestCase
  include TestData

  def app
    Sinatra::Application
  end

end
