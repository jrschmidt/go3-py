# Tests for Legal Moves Methods
class LegalMovesTest < Test::Unit::TestCase
  include TestHelpers
  include TestData


  def test_find_legal_moves
    stones = Stones.new "yes"
    board = BoardSpecs.new
    analyzer = GroupAnalyzer.new(stones, board)
    legal_moves = LegalMovesFinder.new(stones, board, analyzer)

    set_test_groups(stones,3)

    red_moves = legal_moves.find_legal_moves(:red, stones)
    white_moves = legal_moves.find_legal_moves(:white, stones)
    blue_moves = legal_moves.find_legal_moves(:blue, stones)

    assert_equal red_moves.size, 45
    assert_equal white_moves.size, 46
    assert_equal blue_moves.size, 44

    # Most Important Test Points:
    assert red_moves.include?([5,1])
    assert white_moves.include?([5,1])
    assert blue_moves.include?([5,1])

    assert red_moves.include?([5,6])
    assert white_moves.include?([5,6])
    assert blue_moves.include?([5,6])

    assert red_moves.include?([9,4])
    assert white_moves.include?([9,4])
    assert blue_moves.include?([9,4])

    assert red_moves.include?([2,2])
    assert white_moves.include?([2,2])
    refute blue_moves.include?([2,2])

    assert red_moves.include?([1,3])
    assert white_moves.include?([1,3])
    refute blue_moves.include?([1,3])

    refute red_moves.include?([7,6])
    assert white_moves.include?([7,6])
    assert blue_moves.include?([7,6])

    # Other Points:
    assert red_moves.include?([2,7])
    assert white_moves.include?([2,7])
    assert blue_moves.include?([2,7])

    assert red_moves.include?([9,7])
    assert white_moves.include?([9,7])
    assert blue_moves.include?([9,7])

    assert red_moves.include?([11,6])
    assert white_moves.include?([11,6])
    assert blue_moves.include?([11,6])

    assert red_moves.include?([6,11])
    assert white_moves.include?([6,11])
    assert blue_moves.include?([6,11])

    assert red_moves.include?([10,11])
    assert white_moves.include?([10,11])
    assert blue_moves.include?([10,11])

    assert red_moves.include?([7,9])
    assert white_moves.include?([7,9])
    assert blue_moves.include?([7,9])

    refute red_moves.include?([3,2])
    refute white_moves.include?([3,2])
    refute blue_moves.include?([3,2])

    refute red_moves.include?([1,4])
    refute white_moves.include?([1,4])
    refute blue_moves.include?([1,4])

    refute red_moves.include?([6,4])
    refute white_moves.include?([6,4])
    refute blue_moves.include?([6,4])

    refute red_moves.include?([5,5])
    refute white_moves.include?([5,5])
    refute blue_moves.include?([5,5])

    refute red_moves.include?([2,6])
    refute white_moves.include?([2,6])
    refute blue_moves.include?([2,6])
  end


end
